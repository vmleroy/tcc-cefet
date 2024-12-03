import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.Arrays;
import java.nio.file.Path;
import java.io.File;

import engine.core.MarioGame;
import engine.core.MarioResult;
import engine.helper.GameStatus;

public class PlayLevel_v1 {
    public static void printResults(MarioResult result) {
        System.out.println("****************************************************************" + "\n"
                + "Game Status: " + result.getGameStatus().toString() + "\n"
                + "Percentage Completion: " + result.getCompletionPercentage() + "\n"
                + "Remaining Time: " + (int) Math.ceil(result.getRemainingTime() / 1000f)
                + "\n\n"

                + "Lives: " + result.getCurrentLives() + "\n"
                + "Coins: " + result.getCurrentCoins()
                + "\n\n"

                + "Mario State: " + result.getMarioMode() + "\n"
                + "(Mushrooms: " + result.getNumCollectedMushrooms() + " Fire Flowers: "
                + result.getNumCollectedFireflower() + ")"
                + "\n\n"

                + "Total Kills: " + result.getKillsTotal() + "\n"
                + "(Stomps: " + result.getKillsByStomp() + " Fireballs: " + result.getKillsByFire()
                + " Shells: " + result.getKillsByShell() + " Falls: " + result.getKillsByFall() + ")"
                + "\n\n"

                + "Bricks: " + result.getNumDestroyedBricks() + "\n"
                + "Jumps: " + result.getNumJumps() + "\n"
                + "Max X Jump: " + result.getMaxXJump() + "\n"
                + "Max Air Time: " + result.getMaxJumpAirTime() + "\n"
                + "****************************************************************" + "\n");
    }

    public static String getLevel(String filepath) {
        String content = "";
        try {
            content = new String(Files.readAllBytes(Paths.get(filepath)));
        } catch (IOException e) {
        }
        return content;
    }

    public static Boolean saveResults(MarioResult result, String filepath, String fileName) {
        try {
            Path path = Paths.get(filepath);
            if (!Files.exists(path)) {
                Files.createDirectories(path);
            }

            path = Paths.get(filepath + fileName);
            String content = new String(
                    "****************************************************************" + "\n"
                            + "Game Status: " + result.getGameStatus().toString() + "\n"
                            + "Percentage Completion: " + result.getCompletionPercentage() + "\n"
                            + "Remaining Time: " + (int) Math.ceil(result.getRemainingTime() / 1000f)
                            + "\n\n"

                            + "Lives: " + result.getCurrentLives() + "\n"
                            + "Coins: " + result.getCurrentCoins()
                            + "\n\n"

                            + "Mario State: " + result.getMarioMode() + "\n"
                            + "(Mushrooms: " + result.getNumCollectedMushrooms() + " Fire Flowers: "
                            + result.getNumCollectedFireflower() + ")"
                            + "\n\n"

                            + "Total Kills: " + result.getKillsTotal() + "\n"
                            + "(Stomps: " + result.getKillsByStomp() + " Fireballs: " + result.getKillsByFire()
                            + " Shells: " + result.getKillsByShell() + " Falls: " + result.getKillsByFall() + ")"
                            + "\n\n"

                            + "Bricks: " + result.getNumDestroyedBricks() + "\n"
                            + "Jumps: " + result.getNumJumps() + "\n"
                            + "Max X Jump: " + result.getMaxXJump() + "\n"
                            + "Max Air Time: " + result.getMaxJumpAirTime() + "\n"
                            + "****************************************************************" + "\n");

            Files.write(path, content.getBytes());
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    public static Boolean saveMap(String map, String filepath, String fileName) {
        try {
            Path path = Paths.get(filepath);
            if (!Files.exists(path)) {
                Files.createDirectories(path);
            }

            path = Paths.get(filepath + fileName);
            Files.write(path, map.getBytes());
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    public static String concatenateSamples(String[] samples) {
        String level = "";

        String[] splittedLevel = new String[14];
        for (int i = 0; i < samples.length; i++) {
            String[] lines = samples[i].split("\n");
            for (int j = 0; j < lines.length; j++) {
                if (splittedLevel[j] == null) {
                    splittedLevel[j] = lines[j];
                } else {
                    splittedLevel[j] += lines[j];
                }
            }
        }

        for (int i = 0; i < splittedLevel.length; i++) {
            level += splittedLevel[i] + "\n";
        }

        return level;
    }

    public static void main(String[] args) {
        MarioGame game = new MarioGame();
        // printResults(game.playGame(getLevel("../levels/original/lvl-1.txt"), 200,
        // 0));
        // printResults(game.runGame(new agents.robinBaumgarten.Agent(),
        // getLevel("./levels/original/lvl-1.txt"), 20, 0, true));

        String pathToDirectory = "";
        String useOfAI = "default";

        System.out.println("args: " + args.length);

        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("-d")) {
                pathToDirectory = args[i + 1].trim();
            } else if (args[i].equals("-ai")) {
                useOfAI = args[i + 1].trim();
            }
        }

        String folderPath = pathToDirectory != ""
                ? useOfAI.equals("default")
                        ? (System.getProperty("user.dir") + "/" + pathToDirectory + "/generator_results/translated")
                        : (System.getProperty("user.dir") + "/" + pathToDirectory
                                + "/generator_results/gan_generated_translated")
                : System.getProperty("user.dir") + "/src/data/mario/vglc";
        File folder = new File(folderPath);
        File[] listOfFiles = folder.listFiles();
        Arrays.sort(listOfFiles, (a, b) -> {
            String[] aSplit = a.getName().split("_");
            String[] bSplit = b.getName().split("_");
            return Integer.parseInt(aSplit[1].split(".txt")[0]) - Integer.parseInt(bSplit[1].split(".txt")[0]);
        });

        MarioResult[] sampleResults = new MarioResult[listOfFiles.length];

        Integer timer = 60;
        Integer repeatSameLevel = 10;
        Integer complete_levels_index = 0;

        String[] completeLevel = null;

        for (int i = 0; i < listOfFiles.length; i++) {
            System.out.println("Playing level: " + listOfFiles[i].getName() + " " + listOfFiles[i].getPath());
            String level = getLevel(listOfFiles[i].getPath());

            // results[i] = game.runGame(new agents.robinBaumgarten.Agent(), level, timer,
            // 0);
            // results[i] = game.playGame(level, timer, 0);

            // Run only the sample to check if it is winnable
            MarioResult sampleResult = null;
            for (int j = 0; j < repeatSameLevel; j++) {
                sampleResult = game.runGame(new agents.robinBaumgarten.Agent(), level, timer, 0);
                if (sampleResult.getGameStatus() == GameStatus.WIN) {
                    break;
                }
            }
            sampleResults[i] = sampleResult;
            System.out.println("Sample result: " + listOfFiles[i].getName());
            saveResults(sampleResults[i],
                    useOfAI.equals("default")
                            ? System.getProperty("user.dir") + "/" + pathToDirectory + "/generator_results/translated_logs/"
                            : System.getProperty("user.dir") + "/" + pathToDirectory
                                    + "/generator_results/gan_generated_translated_logs/",
                    listOfFiles[i].getName());
            printResults(sampleResults[i]);

            /**
             * If the sample is winnable, run the game again concatenating with other
             * samples that are winnable
             * Then check if the concatenated level is winnable
             * If it is winnable, save the results
             * Else, keep the completeLevel as it is
             */

            if (sampleResult.getGameStatus() == GameStatus.WIN) {
                String[] completeLevelDuplicate = completeLevel;

                if (completeLevelDuplicate == null) {
                    completeLevelDuplicate = new String[1];
                    completeLevelDuplicate[0] = level;
                } else {
                    String[] temp = new String[completeLevelDuplicate.length + 1];
                    for (int j = 0; j < completeLevelDuplicate.length; j++) {
                        System.out.println("level: " + completeLevelDuplicate[j]);
                        temp[j] = completeLevelDuplicate[j];
                    }
                    temp[completeLevelDuplicate.length] = level;
                    completeLevelDuplicate = temp;
                }

                String completeLevelString = concatenateSamples(completeLevelDuplicate);
                System.out.println("Complete level: \n" + completeLevelString);
                MarioResult completeResult = null;

                for (int j = 0; j < repeatSameLevel; j++) {
                    completeResult = game.runGame(new agents.robinBaumgarten.Agent(), completeLevelString, timer, 0);
                    if (completeResult.getGameStatus() == GameStatus.WIN) {
                        completeLevel = completeLevelDuplicate;
                        break;
                    }
                }
            }

            /**
             * If the completeLevel have a size of 10, save the results and reset the
             * completeLevel
             */
            if (completeLevel != null && completeLevel.length == 10) {
                String completeLevelString = concatenateSamples(completeLevel);
                System.out.println("Complete level: \n" + completeLevelString);
                MarioResult completeResult = game.runGame(new agents.robinBaumgarten.Agent(), completeLevelString,
                        timer, 0);
                saveResults(completeResult,
                        useOfAI.equals("default")
                                ? System.getProperty("user.dir") + "/" + pathToDirectory + "/generator_results/complete_levels/"
                                : System.getProperty("user.dir") + "/" + pathToDirectory
                                        + "/generator_results/gan_generated_complete_levels/",
                        "log_complete_" + complete_levels_index + ".txt");
                saveMap(completeLevelString,
                        useOfAI.equals("default")
                                ? System.getProperty("user.dir") + "/" + pathToDirectory + "/generator_results/complete_levels/"
                                : System.getProperty("user.dir") + "/" + pathToDirectory
                                        + "/generator_results/gan_generated_complete_levels/",
                        "lvl_complete_" + complete_levels_index + ".txt");
                complete_levels_index++;
                completeLevel = null;
            }
        }
    }
}
