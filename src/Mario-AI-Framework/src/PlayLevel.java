import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.nio.file.Path;
import java.io.File;

import engine.core.MarioGame;
import engine.core.MarioResult;
import engine.helper.GameStatus;
import thread.GameRunnable;

public class PlayLevel {
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
        String pathToDirectory = "";
        String useOfAI = "default";
        Integer numberOfThreads = 10;

        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "-directory":
                    pathToDirectory = args[i + 1].trim();
                    break;
                case "-ai":
                    useOfAI = args[i + 1].trim();
                    break;
                default:
                    break;
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
        for (int i = 0; i < listOfFiles.length; i++) {
            if (listOfFiles[i].isFile()) {
                System.out.println("File " + listOfFiles[i].getName());
            }
        }
        Arrays.sort(listOfFiles, (a, b) -> {
            String[] aSplit = a.getName().split("_");
            String[] bSplit = b.getName().split("_");
            return Integer.parseInt(aSplit[1].split(".txt")[0]) - Integer.parseInt(bSplit[1].split(".txt")[0]);
        });

        Integer timer = 10;

        Thread[] threads = new Thread[numberOfThreads];
        GameRunnable[] runnables = new GameRunnable[numberOfThreads];

        for (int i = 0; i < numberOfThreads; i++) {
            runnables[i] = new GameRunnable();
            runnables[i].setTimer(timer);
            threads[i] = null;
        }

        for (int i = 0; i < listOfFiles.length; i++) {
            String level = getLevel(listOfFiles[i].getPath());

            /**
             * Run samples to check if they are playable
             */
            for (int j = 0; j < numberOfThreads; j++) {
                if (threads[j] == null || !threads[j].isAlive()) {
                    runnables[j].setLevel(level);
                    threads[j] = new Thread(runnables[j]);
                    threads[j].start();
                    break;
                }
            }

            try {
                for (int j = 0; j < numberOfThreads; j++) {
                    if (threads[j] != null && threads[j].isAlive()) {
                        threads[j].join();
                    }
                }

                MarioResult result = null;
                for (int j = 0; j < numberOfThreads; j++) {
                    if (threads[j] != null && !threads[j].isAlive()) {
                        result = runnables[j].getResult();
                        if (result.getGameStatus() == GameStatus.WIN) {
                            System.out.println("Sample result: " + listOfFiles[i].getName());
                            saveResults(result,
                                    useOfAI.equals("default")
                                            ? System.getProperty("user.dir") + "/" + pathToDirectory
                                                    + "/generator_results/translated_logs/"
                                            : System.getProperty("user.dir") + "/" + pathToDirectory
                                                    + "/generator_results/gan_generated_translated_logs/",
                                    listOfFiles[i].getName());
                            printResults(result);
                            break;
                        }
                        break;
                    }
                }

                System.out.println("Sample result: " + listOfFiles[i].getName());
                saveResults(result,
                        useOfAI.equals("default")
                                ? System.getProperty("user.dir") + "/" + pathToDirectory
                                        + "/generator_results/translated_logs/"
                                : System.getProperty("user.dir") + "/" + pathToDirectory
                                        + "/generator_results/gan_generated_translated_logs/",
                        listOfFiles[i].getName());
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }

    }
}
