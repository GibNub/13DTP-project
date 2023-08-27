/*
  Warnings:

  - Added the required column `answer` to the `FalseAnswer` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_FalseAnswer" (
    "false_answer_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "question_id" INTEGER,
    "answer" TEXT NOT NULL,
    CONSTRAINT "FalseAnswer_question_id_fkey" FOREIGN KEY ("question_id") REFERENCES "Question" ("question_id") ON DELETE SET NULL ON UPDATE CASCADE
);
INSERT INTO "new_FalseAnswer" ("false_answer_id", "question_id") SELECT "false_answer_id", "question_id" FROM "FalseAnswer";
DROP TABLE "FalseAnswer";
ALTER TABLE "new_FalseAnswer" RENAME TO "FalseAnswer";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
