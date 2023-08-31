/*
  Warnings:

  - You are about to drop the `UserScore` table. If the table is not empty, all the data it contains will be lost.

*/
-- DropTable
PRAGMA foreign_keys=off;
DROP TABLE "UserScore";
PRAGMA foreign_keys=on;

-- CreateTable
CREATE TABLE "Score" (
    "score_id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "user_id" INTEGER NOT NULL,
    "quiz_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    "time" INTEGER NOT NULL,
    CONSTRAINT "Score_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "Score_quiz_id_fkey" FOREIGN KEY ("quiz_id") REFERENCES "Quiz" ("quiz_id") ON DELETE RESTRICT ON UPDATE CASCADE
);
