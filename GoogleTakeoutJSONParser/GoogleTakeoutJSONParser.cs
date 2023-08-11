namespace GoogleTakeoutJSONParser
{
    using System;
    using System.IO;
    using Newtonsoft.Json;
    using TakeoutModel;
    public class GoogleTakeoutJSONParser
    {
        string Path{get;}
        public TakeoutData? TakeoutData { get => takeoutData;  }

        TakeoutData? takeoutData;

        public GoogleTakeoutJSONParser(string path){

            Path = path;

            if(!File.Exists(Path)){
                throw new FileNotFoundException("File not found",Path);
            }

            try {
                takeoutData = JsonConvert.DeserializeObject<TakeoutData>(File.ReadAllText(Path));
            } catch (Exception e){
                throw new Exception("Error parsing JSON",e);
            }

        }

        public DateTime GetTakenDateTime(){

            
            long unix_seconds = long.Parse(TakeoutData.PhotoTakenTime.Timestamp);

            return DateTimeOffset.FromUnixTimeSeconds(unix_seconds).DateTime;
           
           
            
            
        }
        
    }
}
