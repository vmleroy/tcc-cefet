import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Arrays;

import engine.core.MarioResult;
import engine.helper.GameStatus;
import runnables.GameRunnable;

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

  private Boolean saveLevelLogResults(MarioResult result, String filepath, String fileName, String samples) {
    try {
      Path path = Paths.get(filepath);
      if (!Files.exists(path)) {
        Files.createDirectories(path);
      }

      path = Paths.get(filepath + fileName);
      String content = new String(""
          + "Map Samples: " + samples + "\n"
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

  public void executeGenerateLevelsWithWinSamples(Integer timer) {
    GameRunnable[] runnables = setThreadRunnables(timer);

    /**
     * Check if generated samples already exist
     */
    String folderPath = useOfAI.equals("default")
        ? (System.getProperty("user.dir") + "/" + this.pathToDirectory + "/generator_results/translated_logs")
        : (System.getProperty("user.dir") + "/" + this.pathToDirectory
            + "/generator_results/gan_generated_translated_logs");
    File folder = new File(folderPath);
    File[] samples = folder.listFiles();

    if (samples.length == this.files.length) {
      System.out.println("All samples have been generated.");
      Arrays.sort(samples, (a, b) -> {
        String[] aSplit = a.getName().split("_");
        String[] bSplit = b.getName().split("_");
        return Integer.parseInt(aSplit[1].split(".txt")[0]) - Integer.parseInt(bSplit[1].split(".txt")[0]);
      });
    } else {
      System.out.println("Some samples are missing. Please run the samples execution first.");
      return;
    }

    /**
     * Filter the samples to get only the winning ones
     */
    File[] winningSamples = null;
    for (int i = 0; i < samples.length; i++) {
      String content = getLevel(samples[i].getPath());
      if (content.contains("Game Status: WIN")) {
        if (winningSamples == null) {
          winningSamples = new File[1];
          winningSamples[0] = samples[i];
        } else {
          File[] temp = new File[winningSamples.length + 1];
          for (int j = 0; j < winningSamples.length; j++) {
            temp[j] = winningSamples[j];
          }
          temp[winningSamples.length] = samples[i];
          winningSamples = temp;
        }
      }
    }

    String[] completeLevel = null;
    String[] mapSamples = new String[10];
    Integer mapSamplesIndex = 0;
    Integer completeLevelsIndex = 0;

    /**
     * Generate levels with winning samples
     */
    for (int i = 0; i < winningSamples.length; i++) {
      Integer fileIndex = 0;
      for (int j = 0; j < this.files.length; j++) {
        if (winningSamples[i].getName().equals(this.files[j].getName())) {
          fileIndex = j;
          break;
        }
      }

      String[] completeLevelDuplicate = completeLevel;
      String level = getLevel(this.files[fileIndex].getPath());

      if (completeLevelDuplicate == null) {
        completeLevelDuplicate = new String[1];
        completeLevelDuplicate[0] = level;
      } else {
        String[] temp = new String[completeLevelDuplicate.length + 1];
        for (int j = 0; j < completeLevelDuplicate.length; j++) {
          temp[j] = completeLevelDuplicate[j];
        }
        temp[completeLevelDuplicate.length] = level;
        completeLevelDuplicate = temp;
      }

      String duplicateCompleteLevelString = concatenateSamples(completeLevelDuplicate);
      MarioResult result = null;
      for (int j = 0; j < numberOfThreads; j++) {
        if (threads[j] == null || !threads[j].isAlive()) {
          runnables[j].setLevel(duplicateCompleteLevelString);
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

        for (int j = 0; j < numberOfThreads; j++) {
          if (threads[j] != null && !threads[j].isAlive()) {
            result = runnables[j].getResult();
            if (result.getGameStatus() == GameStatus.WIN) {
              completeLevel = completeLevelDuplicate;
              mapSamples[mapSamplesIndex] = winningSamples[i].getName();
              mapSamplesIndex++;

              break;
            }
            break;
          }
        }
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }

      if (completeLevel != null && completeLevel.length == 10) {
        String completeLevelString = concatenateSamples(completeLevel);
        String mapSamplesString = "";
        for (int j = 0; j < mapSamples.length; j++) {
          if (mapSamples[j] != null && j < mapSamples.length - 1) {
            mapSamplesString += mapSamples[j] + ", ";
          } else if (mapSamples[j] != null) {
            mapSamplesString += mapSamples[j];
          } else {
            break;
          }
        }

        saveLevelLogResults(result,
            useOfAI.equals("default")
                ? System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/complete_levels_winnable_samples/"
                : System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/gan_generated_complete_levels_winnable_samples/",
            "lvl_complete_" + completeLevelsIndex + "_log" + ".txt", mapSamplesString);

        saveMap(completeLevelString,
            useOfAI.equals("default")
                ? System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/complete_levels_winnable_samples/"
                : System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/gan_generated_complete_levels_winnable_samples/",
            "lvl_complete_" + completeLevelsIndex + "_map" + ".txt");

        completeLevelsIndex++;
        mapSamplesIndex = 0;
        completeLevel = null;
      }
    }
  }

  public void executeGenerateLevelsWithAllSamples(Integer timer) {
    GameRunnable[] runnables = setThreadRunnables(timer);

    String[] completeLevel = null;
    String[] mapSamples = new String[10];
    Integer mapSamplesIndex = 0;
    Integer completeLevelsIndex = 0;

    /**
     * Generate levels with winning samples
     */
    for (int i = 0; i < this.files.length; i++) {
      String[] completeLevelDuplicate = completeLevel;
      String level = getLevel(this.files[i].getPath());

      if (completeLevelDuplicate == null) {
        completeLevelDuplicate = new String[1];
        completeLevelDuplicate[0] = level;
      } else {
        String[] temp = new String[completeLevelDuplicate.length + 1];
        for (int j = 0; j < completeLevelDuplicate.length; j++) {
          temp[j] = completeLevelDuplicate[j];
        }
        temp[completeLevelDuplicate.length] = level;
        completeLevelDuplicate = temp;
      }

      String duplicateCompleteLevelString = concatenateSamples(completeLevelDuplicate);
      MarioResult result = null;
      for (int j = 0; j < numberOfThreads; j++) {
        if (threads[j] == null || !threads[j].isAlive()) {
          runnables[j].setLevel(duplicateCompleteLevelString);
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

        for (int j = 0; j < numberOfThreads; j++) {
          if (threads[j] != null && !threads[j].isAlive()) {
            result = runnables[j].getResult();
            if (result.getGameStatus() == GameStatus.WIN) {
              completeLevel = completeLevelDuplicate;
              mapSamples[mapSamplesIndex] = this.files[i].getName();
              mapSamplesIndex++;

              break;
            }
            break;
          }
        }
      } catch (InterruptedException e) {
        throw new RuntimeException(e);
      }

      if (completeLevel != null && completeLevel.length == 10) {
        String completeLevelString = concatenateSamples(completeLevel);
        String mapSamplesString = "";
        for (int j = 0; j < mapSamples.length; j++) {
          if (mapSamples[j] != null && j < mapSamples.length - 1) {
            mapSamplesString += mapSamples[j] + ", ";
          } else if (mapSamples[j] != null) {
            mapSamplesString += mapSamples[j];
          } else {
            break;
          }
        }

        saveLevelLogResults(result,
            useOfAI.equals("default")
                ? System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/complete_levels_all_samples/"
                : System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/gan_generated_complete_levels_all_samples/",
            "lvl_complete_" + completeLevelsIndex + "_log" + ".txt", mapSamplesString);

        saveMap(completeLevelString,
            useOfAI.equals("default")
                ? System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/complete_levels_all_samples/"
                : System.getProperty("user.dir") + "/" + pathToDirectory
                    + "/generator_results/gan_generated_complete_levels_all_samples/",
            "lvl_complete_" + completeLevelsIndex + "_map" + ".txt");

        completeLevelsIndex++;
        mapSamplesIndex = 0;
        completeLevel = null;
      }
    }
  }
}
