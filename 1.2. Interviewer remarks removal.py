Input text is a conversation history between an interviewer and a respondent. Verify text elements for respondent ownership and filter out elements belonging to the interviewer.

INPUT FORMAT:
IMPORTANT: The incoming text contains a number in the format chunk_id X.Y. Preserve this information in the result and do not delete it during processing.

PROCESSING RULES:
Verify each sentence for:
a. Questions to respondent from interviewer (researcher or AI)
b. Comments from interviewer (researcher or AI) on respondent's answers
c. Respondent's answers
After verifying each sentence, keep only respondent's answers, excluding a. and b. from the text.
If the meaning of respondent's answer is unclear without the interviewer's question or comment, add relevant parts of interviewer's question or comment as context to the respondent's answer.
For example: Interviewer: "How old are you?" Respondent: "20." should be changed to "I am 20 years old," because "20" alone lacks context.
Find respondent's name in the text (if present) and assign it to all respondent's answers, replacing any "Speaker N" (if such title exists) with the corresponding respondent's name.
Maintain existing paragraph format and respondent name title before their answers if such title exists. If no title exists, assign respondent name title to the answer paragraph and remove interviewer's questions and comments while preserving their context in the answers if such context is confirmed by respondent in the conversation.
Finally, verify that all respondent's answers are present and clear in the context of asked questions, and none of the respondent's answers or remarks have been omitted in your response.
Maintain timestamps and speaker indicators e.g. (Speaker X | time) or (хх.yy.zz) related to specific sentences in the result

POST-PROCESSING CHECK:
Ensure that the chunk number (X.Y) is preserved and readable.
Ensure that the cleaned text retains:
- The main meaning of the dialogue
- Individual speech characteristics
- Emotional markers
- Correct sequence of replies
Preserve all timestamps and speaker indications, e.g. (Speaker X | time) or (хх.yy.zz) in related sentences in the result

Finally, check each sentence for completeness, meaning, text coherence, and comprehensibility at first reading.

OUTPUT FORMAT:
The result MUST be in JSON string format with mandatory fields chunk_id X.Y and text according to the input format and fields: "chunk_id": "X.Y", "text": "cleaned_text", where cleaned_text is strictly in English!
Ensure that chunk_id matches the original.

!The result must be strictly in English!