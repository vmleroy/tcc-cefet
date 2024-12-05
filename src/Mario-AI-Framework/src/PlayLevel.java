import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Arrays;
import java.nio.file.Path;
import java.io.File;

public class PlayLevel {
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
        String execution = "samples";

        for (int i = 0; i < args.length; i++) {
            switch (args[i]) {
                case "-directory":
                    pathToDirectory = args[i + 1].trim();
                    break;
                case "-ai":
                    useOfAI = args[i + 1].trim();
                    break;
                case "-execution":
                    execution = args[i + 1].trim();
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

        AlgorithmExecution algorithm = new AlgorithmExecution(listOfFiles, useOfAI, pathToDirectory, numberOfThreads);
        switch (execution) {
            case "samples":
                algorithm.executeOnlySamples(10);
                break;
            default:
                break;
        }

    }
}
