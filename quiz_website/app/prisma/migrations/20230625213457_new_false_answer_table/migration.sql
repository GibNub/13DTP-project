-- CreateTable
CREATE TABLE "FalseAnswer" (
    "false_answer_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "question_id" INTEGER,
    CONSTRAINT "FalseAnswer_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "Question" ("question_id") ON DELETE SET NULL ON UPDATE CASCADE
);
