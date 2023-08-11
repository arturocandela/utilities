namespace GoogleTakeoutJSONParser.TakeoutModel
{

    using Newtonsoft.Json;
    public class TakeoutData
    {
        public string Title { get; set; }
        public string Description { get; set; }
        [JsonProperty("imageViews")]
        public string ImageViews { get; set; }
        public TimeInfo CreationTime { get; set; }
        public TimeInfo PhotoTakenTime { get; set; }
        public GeoDataInfo GeoData { get; set; }
        public GeoDataInfo GeoDataExif { get; set; }
        public string Url { get; set; }
        [JsonProperty("googlePhotosOrigin")]
        public GooglePhotosOriginInfo GooglePhotosOrigin { get; set; }
        public TimeInfo PhotoLastModifiedTime { get; set; }
    }

}