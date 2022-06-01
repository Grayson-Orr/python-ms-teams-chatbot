# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import (
    TextPrompt,
    ConfirmPrompt,
    PromptOptions,
)
from botbuilder.core import MessageFactory, UserState
from pyodbc import connect

from data_models import Survey


class SurveyDialog(ComponentDialog):
    def __init__(self, user_state: UserState, conn_string: str):
        super(SurveyDialog, self).__init__(SurveyDialog.__name__)

        self.survey_accessor = user_state.create_property("Survey")
        self.conn_string = conn_string

        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.question_one_step,
                    self.question_two_step,
                    self.confirm_step,
                    self.summary_step,
                ],
            )
        )
        self.add_dialog(TextPrompt(TextPrompt.__name__))
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))

        self.initial_dialog_id = WaterfallDialog.__name__

    async def question_one_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(
                "Question one placeholder")),
        )

    async def question_two_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        step_context.values["question_one"] = step_context.result

        return await step_context.prompt(
            TextPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text(
                "Question two placeholder")),
        )

    async def confirm_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        step_context.values["question_two"] = step_context.result
        return await step_context.prompt(
            ConfirmPrompt.__name__,
            PromptOptions(prompt=MessageFactory.text("Are you happy with your answers?")),
        )

    async def summary_step(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        if step_context.result:
            survey = await self.survey_accessor.get(
                step_context.context, Survey
            )
            survey.question_one = step_context.values["question_one"]
            survey.question_two = step_context.values["question_two"]

            with connect(self.conn_string) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO Survey (QuestionOne, QuestionTwo) VALUES (?, ?)  
                    """, survey.question_one, survey.question_two)
                    conn.commit()

        await step_context.context.send_activity(
            MessageFactory.text("Thank you for completing the survey. We appreciate your feedback.")
        )

        return await step_context.end_dialog()
