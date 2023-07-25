package utilidades;

import java.io.File;
import java.io.FilenameFilter;
import java.util.zip.ZipFile;

public class FileUtilities {

    public static File[] GetZipFiles(String path) {
        File directory = new File(path);
        File[] files = directory.listFiles(new FilenameFilter() {
            @Override
            public boolean accept(File dir, String name) {
                return name.toLowerCase().endsWith(".zip");
            }
        });

        return files;
    }

    public static File[] GetFileJsonsInsideZipFile(File zipFile){

        File[] files = null;

        try (ZipFile zipFile = new ZipFile(archivoZip)) {
            Enumeration<? extends ZipEntry> entries = zipFile.entries();
            while (entries.hasMoreElements()) {
                ZipEntry entry = entries.nextElement();
                if (entry.getName().toLowerCase().endsWith(".json")) {
                    Path path = Paths.get(relPath).resolve(entry.getName());
                    Files.createDirectories(path.getParent());
                    zipFile.getInputStream(entry).transferTo(Files.newOutputStream(path));
                }
            }
        }
        

    }



    
}
