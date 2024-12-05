import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

import engine.core.MarioResult;
import engine.helper.GameStatus;
import thread.GameRunnable;

public class AlgorithmExecution {
  private File[] files;
  private String useOfAI;
  private String pathToDirectory;
  private Integer numberOfThreads;

  Thread[] threads;

  public AlgorithmExecution(File[] files, String useOfAI, String pathToDirectory, Integer numberOfThreads) {
    this.files = files;
    this.useOfAI = useOfAI;
    this.pathToDirectory = pathToDirectory;
    this.numberOfThreads = numberOfThreads;
    this.threads = new Thread[numberOfThreads];
  }

  private void printResults(MarioResult result) {
    System.out.println(""
        + "****************************************************************" + "\n"
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

  private Boolean saveSampleLogResults(MarioResult result, String filepath, String fileName) {
    try {
      Path path = Paths.get(filepath);
      if (!Files.exists(path)) {
        Files.createDirectories(path);
      }

      path = Paths.get(filepath + fileName);
      String content = new String(""
          + "****************************************************************" + "\n"
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

  public static String getLevel(String filepath) {
    String content = "";
    try {
      content = new String(Files.readAllBytes(Paths.get(filepath)));
    } catch (IOException e) {
    }
    return content;
  }

  private GameRunnable[] setThreadRunnables(Integer timer) {
    GameRunnable[] runnables = new GameRunnable[this.numberOfThreads];
    for (int i = 0; i < numberOfThreads; i++) {
      runnables[i] = new GameRunnable();
      runnables[i].setTimer(timer);
      this.threads[i] = null;
    }
    return runnables;
  }

  public void executeOnlySamples(Integer timer) {
    GameRunnable[] runnables = setThreadRunnables(timer);

    for (int i = 0; i < this.files.length; i++) {
      String level = getLevel(this.files[i].getPath());

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
              saveSampleLogResults(result,
                  this.useOfAI.equals("default")
                      ? System.getProperty("user.dir") + "/" + pathToDirectory
                          + "/generator_results/translated_logs/"
                      : System.getProperty("user.dir") + "/" + pathToDirectory
                          + "/generator_results/gan_generated_translated_logs/",
                  this.files[i].getName());
              break;
            }
            break;
          }
        }

        saveSampleLogResults(result,
            useOfAI.equals("default")
                ? System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/translated_logs/"
                : System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/gan_generated_translated_logs/",
            this.files[i].getName());
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }
    }
  }
}
