// See https://aka.ms/new-console-template for more information




namespace ArtImageTaggerConsole  {

    using System;
    using System.IO;
    using System.Linq;

    class Program {
    static void Main(string[] args) {

        string directoryPath = ".";
        
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

        foreach (var file in files)
        {
            Console.WriteLine(file);
        }


    }
}

}



