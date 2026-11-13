"""
Interview Answer Evaluator

Version 1:
Rule-based evaluation of candidate answers.

This version evaluates:
- Answer relevance
- Keyword coverage
- Answer completeness
- Overall score
"""


class AnswerEvaluator:
    """Evaluate candidate answers."""

    def __init__(self):
        self.minimum_answer_length = 10

    def calculate_keyword_score(self, answer, expected_keywords):
        """Calculate how many expected keywords appear in the answer."""

        answer_lower = answer.lower()

        if not expected_keywords:
            return 100.0

        matched_keywords = []

        for keyword in expected_keywords:
            if keyword.lower() in answer_lower:
                matched_keywords.append(keyword)

        score = (
            len(matched_keywords) / len(expected_keywords)
        ) * 100

        return score

    def evaluate_answer(
        self,
        question,
        answer,
        expected_keywords
    ):
        """
        Evaluate a candidate answer.

        Returns:
            dict: Evaluation result.
        """

        if not answer or len(answer.strip()) < self.minimum_answer_length:
            return {
                "score": 0,
                "relevance": "Low",
                "completeness": "Low",
                "feedback": "The answer is too short to evaluate properly.",
            }

        keyword_score = self.calculate_keyword_score(
            answer,
            expected_keywords
        )

        # Determine relevance
        if keyword_score >= 70:
            relevance = "High"
        elif keyword_score >= 40:
            relevance = "Medium"
        else:
            relevance = "Low"

        # Determine completeness
        word_count = len(answer.split())

        if word_count >= 50 and keyword_score >= 60:
            completeness = "High"
        elif word_count >= 25 and keyword_score >= 40:
            completeness = "Medium"
        else:
            completeness = "Low"

        # Overall score
        score = (
            (keyword_score * 0.6)
            + (
                min(word_count / 50, 1) * 100 * 0.4
            )
        )

        score = round(min(score, 100), 2)

        # Feedback
        if score >= 80:
            feedback = (
                "Strong answer. The response is relevant and "
                "covers the important concepts."
            )

        elif score >= 60:
            feedback = (
                "Good answer, but it could include more relevant "
                "technical details or examples."
            )

        elif score >= 40:
            feedback = (
                "The answer is partially relevant. "
                "Try to explain the key concepts in more detail."
            )

        else:
            feedback = (
                "The answer needs improvement. "
                "Focus on directly answering the question "
                "and covering the important concepts."
            )

        return {
            "score": score,
            "relevance": relevance,
            "completeness": completeness,
            "keyword_score": round(keyword_score, 2),
            "feedback": feedback,
        }


if __name__ == "__main__":

    question = "What is machine learning?"

    candidate_answer = """
    Machine learning is a field of artificial intelligence where
    computers learn patterns from data and use those patterns
    to make predictions or decisions without being explicitly
    programmed for every task.
    """

    expected_keywords = [
        "machine learning",
        "data",
        "patterns",
        "predictions",
    ]

    evaluator = AnswerEvaluator()

    result = evaluator.evaluate_answer(
        question,
        candidate_answer,
        expected_keywords
    )

    print("\n===== ANSWER EVALUATION =====\n")

    print(f"Question: {question}")

    print(f"\nCandidate Answer:\n{candidate_answer.strip()}")

    print("\n--- Evaluation ---")
    print(f"Score: {result['score']}/100")
    print(f"Relevance: {result['relevance']}")
    print(f"Completeness: {result['completeness']}")
    print(f"Keyword Score: {result['keyword_score']}/100")
    print(f"Feedback: {result['feedback']}")