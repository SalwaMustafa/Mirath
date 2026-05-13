from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
from .AssistantScheme import UserProfile, RoadmapRequirements, ExtractionSchema, RouteQuery, EvaluationResult, AgentState
from .AssistantPrompts import ROUTER_SYSTEM_MESSAGE, GENERAL_ASSISTANT_PROMPT, ROADMAP_GUARDIAN_PROMPT, ROADMAP_SYSTEM_PROMPT, REFLEXION_ROADMAP_PROMPT, REFLEXION_GENERAL_PROMPT
from .AssistantEnum import AssistantEnum
from .Assets import get_research_tools, get_model
import asyncio

class AssistantGraph:

    def __init__(self, memory, sleep_time: int = 5):

        self.llm = get_model()
        self.memory = memory
        self.tools = get_research_tools()
        self.tool_node = ToolNode(self.tools)
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.sleep_time = sleep_time
        self.assistant_graph = self._create_workflow()


    async def router_node(self, state: AgentState):
        """
        Routes incoming questions to either general assistant or specialized roadmap agent.
        Analyzes the user's question to determine if it's:
        - A roadmap/plan request → routes to roadmap_guardian_node
        - A general question → routes to general_assistant_node

        """

        structured_llm = self.llm.with_structured_output(RouteQuery)
        messages  = ROUTER_SYSTEM_MESSAGE.format_messages(messages = state.get("messages", []))
        decision = await structured_llm.ainvoke(messages)
        await asyncio.sleep(self.sleep_time)


        return {"next_step": decision.destination}
    

    async def general_assistant_node(self,state: AgentState):
        """
        Handles general questions using LLM with access to Tavily search and arXiv tools.
        Determines if reflection is needed based on complexity and confidence.

        """

        profile = state.get("user_profile") or UserProfile()

        messages = GENERAL_ASSISTANT_PROMPT.format_messages(
            name=profile.name or "Researcher",
            level=profile.research_level or "Not specified",
            field=profile.field_of_interest or "Not specified",
            language=profile.preferred_language,
            messages = state.get("messages", [])
        )
        
        response = await self.llm_with_tools.ainvoke(messages)
        await asyncio.sleep(self.sleep_time)

        
        return {
            "messages": [response],
            "agent_type": AssistantEnum.GENERAL_ASSISTANT.value,
            "next_step": AssistantEnum.REFLEXION.value
        }
    

    async def roadmap_guardian_node(self, state: AgentState):
        """
        Updates the user's profile and roadmap requirements using structured extraction.
        Asks clarifying questions if required fields (topic, research_level, time_frame) are missing.
        
        """
    
        current_profile = state.get("user_profile") or UserProfile()
        current_reqs = state.get("roadmap_reqs") or RoadmapRequirements()

       
        extractor = self.llm.with_structured_output(ExtractionSchema)
        messages = ROADMAP_GUARDIAN_PROMPT.format_messages(
            topic=current_reqs.topic,
            level=current_profile.research_level,
            time_frame=current_reqs.time_frame,
            field=current_profile.field_of_interest or "Not specified",
            messages = state.get("messages", []))
        
        extraction = await extractor.ainvoke(messages) or ExtractionSchema()
        await asyncio.sleep(self.sleep_time)
        
        updated_profile = UserProfile(
            name = extraction.name or current_profile.name or "Researcher",
            research_level = extraction.research_level or current_profile.research_level,
            field_of_interest = extraction.field_of_interest or current_profile.field_of_interest,
            preferred_language = extraction.preferred_language or current_profile.preferred_language,
            notable_publications = (current_profile.notable_publications or []) + (extraction.notable_publications or [])
        )

        
        updated_reqs = RoadmapRequirements(
            topic=extraction.topic or current_reqs.topic,
            time_frame=extraction.time_frame or current_reqs.time_frame
        )
        
        missing = []
        if not updated_reqs.topic:
            missing.append("topic")
        if not updated_profile.research_level:
            missing.append("research_level")
        if not updated_reqs.time_frame:
            missing.append("time_frame")

        
        if missing:
            questions = []

            if "topic" in missing:
                questions.append(
                    "What specific topic do you want the roadmap for? "
                )

            if "research_level" in missing:
                questions.append(
                    "What is your research level? (Undergraduate, Master's Student, PhD Researcher, Professor)"
                )

            if "time_frame" in missing:
                questions.append(
                    "How much time do you want to dedicate to this roadmap?"
                )

            return {
                "messages": [AIMessage(content="\n".join(questions), additional_kwargs={"type": "guardian"} )],
                "user_profile": updated_profile,
                "roadmap_reqs": updated_reqs,
                "next_step": AssistantEnum.WAIT_USER.value
            }

        
        return {
            "messages": [],
            "user_profile": updated_profile,
            "roadmap_reqs": updated_reqs,
            "next_step": AssistantEnum.ROADMAP_GENERATOR.value
        }
    

    async def roadmap_generator_node(self, state: AgentState):
        """
        Specialized agent for creating comprehensive and reliable roadmaps.
        Utilizes Tavily search and arXiv tools to find and verify seminal papers.
        Ensures a narrative flow connecting the evolution of ideas in the roadmap.

        """
        reqs = state["roadmap_reqs"] or RoadmapRequirements()
        profile = state["user_profile"] or UserProfile()
        
        
        messages = ROADMAP_SYSTEM_PROMPT.format_messages(
            name=profile.name or "Researcher",
            topic=reqs.topic,
            level=profile.research_level,
            time_frame=reqs.time_frame,
            field=profile.field_of_interest or "Not specified",
            language=profile.preferred_language,
            messages = state.get("messages", [])
        )

        response = await self.llm_with_tools.ainvoke(messages)
        await asyncio.sleep(self.sleep_time)
        
        return {
            "messages": [response], 
            "agent_type": AssistantEnum.ROADMAP_GENERATOR.value,
            "next_step": AssistantEnum.REFLEXION.value
        }
    

    async def reflexion_node(self, state: AgentState):
        """
        Reflects on the generated response to ensure quality and reduce hallucinations.
        Only activated when needed for complex queries or important outputs.
        Evaluates the last response based on accuracy, detail, and citations.

        """

        agent_type = state.get("agent_type")
        
        if agent_type == AssistantEnum.ROADMAP_GENERATOR.value:
            messages = REFLEXION_ROADMAP_PROMPT.format_messages(
                research_level = state["user_profile"].research_level,
                field = state["user_profile"].field_of_interest or "Not specified",
                messages = state.get("messages", [])
                )
        else:
            messages = REFLEXION_GENERAL_PROMPT.format_messages(messages = state["messages"])
        
        evaluator = self.llm.with_structured_output(EvaluationResult)
        eval_result = await evaluator.ainvoke(messages)
        await asyncio.sleep(self.sleep_time)
        
        if eval_result.is_satisfactory == AssistantEnum.PASS.value or state.get("reflexion_count", 0) >=1:
            return {"next_step": AssistantEnum.END.value, "reflexion_count": 0}
        
        
        feedback_msg = f"Reflexion Reasoning: {eval_result.reasoning} and Feedback: {eval_result.feedback}."
        return {
            "messages": [HumanMessage(content=feedback_msg,
                                      additional_kwargs={"type": "Reflexion"} )],
            "next_step": AssistantEnum.RETRY.value,
            "reflexion_count": state.get("reflexion_count", 0) + 1,
            "tool_call_count" :0
        }
    
    async def tools_node_wrapper(self, state):
        result = await self.tool_node.ainvoke(state)
        return {
            **result,
            "tool_call_count": state.get("tool_call_count", 0) + 1 
        }
        

    def route_decision(self, state):

        return state["next_step"]
    

    def guardian_decision(self, state):

        if state["next_step"] == AssistantEnum.WAIT_USER.value:
            return END
        return "roadmap_generator"
    

    def post_generation_condition(self, state):

        MAX_TOOL_CALLS = 3
        tool_call_count = state.get("tool_call_count", 0)
    
        last_msg = state["messages"][-1]
        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
            if tool_call_count >= MAX_TOOL_CALLS:
                return "reflexion"  
            return "tools"
        
        return "reflexion"
    

    def tools_decision(self, state: AgentState):
    
        if state.get("agent_type") == AssistantEnum.ROADMAP_GENERATOR.value:
            return "roadmap_generator"
        return "general_assistant"


    def reflexion_decision(self, state: AgentState):

        if state["next_step"] == AssistantEnum.RETRY.value:
            if state.get("agent_type") == AssistantEnum.ROADMAP_GENERATOR.value:
                return "roadmap_generator"
            return "general_assistant"
        
        return END
    

    def _create_workflow(self):

        workflow = StateGraph(AgentState)

    
        workflow.add_node("router", self.router_node)
        workflow.add_node("general_assistant", self.general_assistant_node)
        workflow.add_node("roadmap_guardian", self.roadmap_guardian_node)
        workflow.add_node("roadmap_generator", self.roadmap_generator_node)
        workflow.add_node("reflexion", self.reflexion_node)
        
        
        workflow.add_node("tools", self.tools_node_wrapper)

        workflow.set_entry_point("router")

       
        workflow.add_conditional_edges(
            "router", 
            self.route_decision, 
            {"general_assistant": "general_assistant", "roadmap_guardian": "roadmap_guardian"}
        )
        
        workflow.add_conditional_edges(
            "roadmap_guardian", 
            self.guardian_decision, 
            {"roadmap_generator": "roadmap_generator", END: END}
        )

        workflow.add_conditional_edges(
            "general_assistant", 
            self.post_generation_condition, 
            {"tools": "tools", "reflexion": "reflexion"}
        )

        workflow.add_conditional_edges(
            "roadmap_generator", 
            self.post_generation_condition, 
            {"tools": "tools", "reflexion": "reflexion"}
        )

        workflow.add_conditional_edges(
            "tools", 
            self.tools_decision, 
            {"roadmap_generator": "roadmap_generator", "general_assistant": "general_assistant"}
        )

        workflow.add_conditional_edges(
            "reflexion", 
            self.reflexion_decision, 
            {"roadmap_generator": "roadmap_generator", "general_assistant": "general_assistant", END: END}
        )

        return workflow.compile(checkpointer=self.memory)




