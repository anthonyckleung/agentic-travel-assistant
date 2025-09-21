import os
import psycopg2
from chatbot_ui.core.config import config
from chatbot_ui.retrieval import rag_pipeline

from langsmith import Client

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper


ls_client = Client(api_key=config.LANGSMITH_API_KEY)
conn = psycopg2.connect(
    dbname="postgresdb",
    user=config.POSTGRES_USERNAME,
    password=config.POSTGRES_PASSWORD,
    host="host.docker.internal",  # e.g., "localhost"
    port="5433"        # default PostgreSQL port
)
cursor = conn.cursor()
from ragas.dataset_schema import SingleTurnSample 
from ragas.metrics import Faithfulness, ResponseRelevancy, LLMContextPrecisionWithoutReference, LLMContextRecall, NonLLMContextRecall

ragas_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4.1-mini"))
ragas_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))


async def ragas_faithfulness(run, example):

    sample = SingleTurnSample(
            user_input=run.outputs["question"],
            response=run.outputs["answer"],
            retrieved_contexts=run.outputs["retrieved_context"]
        )
    scorer = Faithfulness(llm=ragas_llm)

    return await scorer.single_turn_ascore(sample)


async def ragas_responce_relevancy(run, example):

    sample = SingleTurnSample(
            user_input=run.outputs["question"],
            response=run.outputs["answer"],
            retrieved_contexts=run.outputs["retrieved_context"]
        )
    scorer = ResponseRelevancy(llm=ragas_llm, embeddings=ragas_embeddings)

    return await scorer.single_turn_ascore(sample)


async def ragas_context_precision(run, example):

    sample = SingleTurnSample(
            user_input=run.outputs["question"],
            response=run.outputs["answer"],
            retrieved_contexts=run.outputs["retrieved_context"]
        )
    scorer = LLMContextPrecisionWithoutReference(llm=ragas_llm)

    return await scorer.single_turn_ascore(sample)


async def ragas_context_recall_llm_based(run, example):

    sample = SingleTurnSample(
            user_input=run.outputs["question"],
            response=run.outputs["answer"],
            reference=example.outputs["ground_truth"],
            retrieved_contexts=run.outputs["retrieved_context"]
        )
    scorer = LLMContextRecall(llm=ragas_llm)

    return await scorer.single_turn_ascore(sample)


async def ragas_context_recall_non_llm(run, example):

    sample = SingleTurnSample(
            retrieved_contexts=run.outputs["retrieved_context"],
            reference_contexts=example.outputs["contexts"]
        )
    scorer = NonLLMContextRecall()

    return await scorer.single_turn_ascore(sample)


results = ls_client.evaluate(
    lambda x: rag_pipeline(x["question"], cursor),
    data="travel-rag-evaluation-dataset",
    evaluators=[
        ragas_faithfulness,
        ragas_responce_relevancy,
        ragas_context_precision,
        ragas_context_recall_llm_based,
        ragas_context_recall_non_llm
    ],
    experiment_prefix="travel-rag-evaluation-dataset"
)