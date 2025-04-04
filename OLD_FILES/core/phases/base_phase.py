import logging

from core.registries.phase_registry import BasePhase
from core.registries.phase_registry import PhaseRegistry
from spark.ai.ai_processor import AIProcessor  # ✅ AI logic now runs through MCC

logger = logging.getLogger(__name__)


class Code_Generation(BasePhase):
    """Executes AI-Powered Code Generation"""

    async def execute(self, input_data):
        logger.info("🛠️ AI Code Generation Executing...")
        ai_output = await AIProcessor.run_ai_model(
            "code_gen", input_data
        )  # ✅ Awaiting AI call
        return {"status": "success", "output": ai_output}


class Automated_Testing(BasePhase):
    """Executes AI-Powered Automated Testing"""

    async def execute(self, input_data):
        logger.info("✅ AI Automated Testing Executing...")
        ai_output = await AIProcessor.run_ai_model(
            "test_generation", input_data
        )  # ✅ Awaiting AI call
        return {"status": "success", "output": ai_output}


class Bug_Fixing(BasePhase):
    """Executes AI-Powered Bug Fixing"""

    async def execute(self, input_data):
        logger.info("🔧 AI Bug Fixing Executing...")
        ai_output = await AIProcessor.run_ai_model(
            "bug_fix", input_data
        )  # ✅ Awaiting AI call
        return {"status": "success", "output": ai_output}


class Career_Pathing_Engine(BasePhase):
    """Executes AI-Powered Career Navigation"""

    async def execute(self, input_data):
        logger.info("🛣️ AI Career Pathing Executing...")
        return AIProcessor.run_ai_model("career_advice", input_data)


class Job_Matching(BasePhase):
    """Executes AI-Driven Job Matching"""

    async def execute(self, input_data):
        logger.info("🔍 AI Job Matching Executing...")
        return AIProcessor.run_ai_model("job_match", input_data)


class Scholarship_Finder(BasePhase):
    """Executes AI-Powered Scholarship Search"""

    async def execute(self, input_data):
        logger.info("🎓 AI Scholarship Finder Executing...")
        return AIProcessor.run_ai_model("scholarship_search", input_data)


class Lead_Scoring_Prioritization(BasePhase):
    """Executes AI-Powered Lead Scoring"""

    async def execute(self, input_data):
        logger.info("📊 AI Lead Scoring Executing...")
        return AIProcessor.run_ai_model("lead_scoring", input_data)


class Personalized_Email_Sequences(BasePhase):
    """Executes AI-Powered Email Sequences"""

    async def execute(self, input_data):
        logger.info("📩 AI Personalized Email Sequence Executing...")
        return AIProcessor.run_ai_model("email_generation", input_data)


class AI_Chatbots_Conversational_Sales(BasePhase):
    """Executes AI-Powered Chatbot Sales"""

    async def execute(self, input_data):
        logger.info("🤖 AI Chatbots Executing...")
        return AIProcessor.run_ai_model("chatbot_sales", input_data)


class Sales_Forecasting_Trend_Analysis(BasePhase):
    """Executes AI-Powered Sales Forecasting"""

    async def execute(self, input_data):
        logger.info("📈 AI Sales Forecasting Executing...")
        return AIProcessor.run_ai_model("sales_forecast", input_data)


class Quota_Compensation_Optimization(BasePhase):
    """Executes AI-Powered Quota & Compensation Optimization"""

    async def execute(self, input_data):
        logger.info("💰 AI Quota & Compensation Optimization Executing...")
        return AIProcessor.run_ai_model("quota_optimization", input_data)


class AI_Powered_Sales_Coaching(BasePhase):
    """Executes AI-Powered Sales Coaching"""

    async def execute(self, input_data):
        logger.info("📈 AI Sales Coaching Executing...")
        return AIProcessor.run_ai_model("sales_coaching", input_data)


class Employee_Retention_Analysis(BasePhase):
    """Executes AI-Powered Employee Retention Analysis"""

    async def execute(self, input_data):
        logger.info("👥 AI Employee Retention Analysis Executing...")
        return AIProcessor.run_ai_model("retention_analysis", input_data)


class Workforce_Performance_Benchmarking(BasePhase):
    """Executes AI-Powered Workforce Benchmarking"""

    async def execute(self, input_data):
        logger.info("📊 AI Workforce Benchmarking Executing...")
        return AIProcessor.run_ai_model("performance_benchmarking", input_data)


class AI_Optimized_Hiring_Recommendations(BasePhase):
    """Executes AI-Driven Hiring Recommendations"""

    async def execute(self, input_data):
        logger.info("👥 AI Hiring Optimization Executing...")
        return AIProcessor.run_ai_model("hiring_recommendations", input_data)


PhaseRegistry.register("Code Generation", Code_Generation)
PhaseRegistry.register("Automated Testing", Automated_Testing)
PhaseRegistry.register("Bug Fixing", Bug_Fixing)
PhaseRegistry.register("Career Pathing Engine", Career_Pathing_Engine)
PhaseRegistry.register("Job Matching", Job_Matching)
PhaseRegistry.register("Scholarship Finder", Scholarship_Finder)
PhaseRegistry.register("Lead Scoring & Prioritization", Lead_Scoring_Prioritization)
PhaseRegistry.register("Personalized Email Sequences", Personalized_Email_Sequences)
PhaseRegistry.register(
    "AI Chatbots & Conversational Sales", AI_Chatbots_Conversational_Sales
)
PhaseRegistry.register(
    "Sales Forecasting & Trend Analysis", Sales_Forecasting_Trend_Analysis
)
PhaseRegistry.register(
    "Quota & Compensation Optimization", Quota_Compensation_Optimization
)
PhaseRegistry.register("AI-Powered Sales Coaching", AI_Powered_Sales_Coaching)
PhaseRegistry.register("Employee Retention Analysis", Employee_Retention_Analysis)
PhaseRegistry.register(
    "Workforce Performance Benchmarking", Workforce_Performance_Benchmarking
)
PhaseRegistry.register(
    "AI-Optimized Hiring Recommendations", AI_Optimized_Hiring_Recommendations
)
