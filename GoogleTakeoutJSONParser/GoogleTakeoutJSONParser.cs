namespace GoogleTakeoutJSONParser
{
    using System;
    using System.IO;
    using Newtonsoft.Json;
    public class GoogleTakeoutJSONParser
    {
        private GoogleTakeoutJSONParser(){

        }

        public static Dictionary<string,object>? getJSON(string path){
            string json = File.ReadAllText(path);
            return JsonConvert.DeserializeObject<Dictionary<string,object>>(json);
        }
        
    }
}
