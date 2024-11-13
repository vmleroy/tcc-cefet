import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.time.Duration;
import java.util.Arrays;
import java.nio.file.Path;
import java.io.File;

import engine.core.MarioGame;
import engine.core.MarioResult;

public class PlayLevel {
    public static void printResults(MarioResult result) {
        System.out.println("****************************************************************");
        System.out.println("Game Status: " + result.getGameStatus().toString() +
                " Percentage Completion: " + result.getCompletionPercentage());
        System.out.println("Lives: " + result.getCurrentLives() + " Coins: " + result.getCurrentCoins() +
                " Remaining Time: " + (int) Math.ceil(result.getRemainingTime() / 1000f));
        System.out.println("Mario State: " + result.getMarioMode() +
                " (Mushrooms: " + result.getNumCollectedMushrooms() + " Fire Flowers: "
                + result.getNumCollectedFireflower() + ")");
        System.out.println("Total Kills: " + result.getKillsTotal() + " (Stomps: " + result.getKillsByStomp() +
                " Fireballs: " + result.getKillsByFire() + " Shells: " + result.getKillsByShell() +
                " Falls: " + result.getKillsByFall() + ")");
        System.out.println("Bricks: " + result.getNumDestroyedBricks() + " Jumps: " + result.getNumJumps() +
                " Max X Jump: " + result.getMaxXJump() + " Max Air Time: " + result.getMaxJumpAirTime());
        System.out.println("****************************************************************");
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
                    "****************************************************************" + "\n" +
                            "Game Status: " + result.getGameStatus().toString() + " Percentage Completion: "
                            + result.getCompletionPercentage() + "\n" +
                            "Lives: " + result.getCurrentLives() + " Coins: " + result.getCurrentCoins() +
                            " Remaining Time: " + (int) Math.ceil(result.getRemainingTime() / 1000f) + "\n" +
                            "Mario State: " + result.getMarioMode() +
                            " (Mushrooms: " + result.getNumCollectedMushrooms() + " Fire Flowers: "
                            + result.getNumCollectedFireflower() + ")" + "\n" +
                            "Total Kills: " + result.getKillsTotal() + " (Stomps: " + result.getKillsByStomp() +
                            " Fireballs: " + result.getKillsByFire() + " Shells: " + result.getKillsByShell() +
                            " Falls: " + result.getKillsByFall() + ")" + "\n" +
                            "Bricks: " + result.getNumDestroyedBricks() + " Jumps: " + result.getNumJumps() +
                            " Max X Jump: " + result.getMaxXJump() + " Max Air Time: " + result.getMaxJumpAirTime()
                            + "\n" +
                            "****************************************************************" + "\n");

            Files.write(path, content.getBytes());
            return true;
        } catch (IOException e) {
            return false;
        }
    }

    public static void main(String[] args) {
        MarioGame game = new MarioGame();
        // printResults(game.playGame(getLevel("../levels/original/lvl-1.txt"), 200,
        // 0));
        // printResults(game.runGame(new agents.robinBaumgarten.Agent(),
        // getLevel("./levels/original/lvl-1.txt"), 20, 0, true));

        String folderPath = args.length > 0
                ? (System.getProperty("user.dir") + "/" + args[0] + "/generator_results/translated")
                : System.getProperty("user.dir") + "/src/data/mario/vglc";
        File folder = new File(folderPath);
        File[] listOfFiles = folder.listFiles();
        Arrays.sort(listOfFiles, (a, b) -> {
            String[] aSplit = a.getName().split("_");
            String[] bSplit = b.getName().split("_");
            return Integer.parseInt(aSplit[1].split(".txt")[0]) - Integer.parseInt(bSplit[1].split(".txt")[0]);
        });

        MarioResult[] results = new MarioResult[listOfFiles.length];

        Integer timer = 60;

        for (int i = 0; i < listOfFiles.length; i++) {
            System.out.println("Playing level: " + listOfFiles[i].getName() + " " + listOfFiles[i].getPath());
            String level = getLevel(listOfFiles[i].getPath());
            results[i] = game.runGame(new agents.robinBaumgarten.Agent(), level, timer, 0);
            // results[i] = game.playGame(level, timer, 0);
            saveResults(results[i],
                    System.getProperty("user.dir") + "/" + args[0] + "/generator_results/translated_logs/",
                    listOfFiles[i].getName());
            printResults(results[i]);
        }
    }
}
