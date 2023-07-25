// See https://aka.ms/new-console-template for more information




namespace ArtImageTaggerConsole  {

    using System;
    using System.IO;
    using System.Linq;

    class Program {
    static void Main(string[] args) {

        string directoryPath = @".";
        
        if (args.Length == 0) {
            Console.WriteLine("Usando ruta por defecto: " + directoryPath);
        } else if (args.Length == 1) {
            directoryPath = args[0];
            Console.WriteLine("Usando ruta: " + directoryPath);
        } else {
            Console.WriteLine("Uso: ArtImageTaggerConsole.exe [ruta]");
            return;
        }

        
        var allowedExtensions = new [] {".jpg",".jpeg"}; 


        var files = Directory.GetFiles(directoryPath, "*.*", SearchOption.AllDirectories)
                             .Where(file => allowedExtensions.Any(file.ToLower().EndsWith));

        string pathToTakeout = @"C:\Users\artur\Desktop\Utilidades\Takeout\Google Fotos\";




        foreach (var file in files)
        {
           string extension = Path.GetExtension(file).ToLower();

           string relativePath = Path.GetRelativePath(directoryPath, file);
            string takeout = Path.Combine(pathToTakeout, relativePath);
            takeout+= ".json";


           switch(extension){
            
            case ".jpg":
            case ".jpeg":
                Dictionary<string,object>? json = null;
                
                try {
                    json = GoogleTakeoutJSONParser.GoogleTakeoutJSONParser.getJSON(takeout);
                } catch (Exception) {
                    
                }

                if (json != null) {
                    Console.WriteLine(file + " - HAS TAKEOUT");
                } else {
                    Console.WriteLine(file);
                }
                
                break;
            default:
                Console.WriteLine("No se reconoce la extensión: " + extension);
                break;

           }
            

        }


    }
}

}



