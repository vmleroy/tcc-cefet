import java.util.Arrays;
import java.io.File;

public class PlayLevel {

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
                algorithm.executeOnlySamples(60);
                break;
            case "levels":
                algorithm.executeGenerateLevelsWithWinSamples(120);
                break;
            case "levels_all_samples":
                algorithm.executeGenerateLevelsWithWinSamples(120);
                break;
            default:
                break;
        }

    }
}
