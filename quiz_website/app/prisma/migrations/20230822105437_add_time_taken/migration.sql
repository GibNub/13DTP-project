/*
  Warnings:

  - Added the required column `time` to the `UserScore` table without a default value. This is not possible if the table is not empty.

*/
-- RedefineTables
PRAGMA foreign_keys=OFF;
CREATE TABLE "new_UserScore" (
    "user_id" INTEGER NOT NULL,
    "quiz_id" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    "time" INTEGER NOT NULL,

    PRIMARY KEY ("user_id", "quiz_id"),
    CONSTRAINT "UserScore_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "User" ("user_id") ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT "UserScore_quiz_id_fkey" FOREIGN KEY ("quiz_id") REFERENCES "Quiz" ("quiz_id") ON DELETE RESTRICT ON UPDATE CASCADE
);
INSERT INTO "new_UserScore" ("quiz_id", "score", "user_id") SELECT "quiz_id", "score", "user_id" FROM "UserScore";
DROP TABLE "UserScore";
ALTER TABLE "new_UserScore" RENAME TO "UserScore";
PRAGMA foreign_key_check;
PRAGMA foreign_keys=ON;
mi