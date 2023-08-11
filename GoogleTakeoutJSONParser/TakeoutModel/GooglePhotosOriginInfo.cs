namespace GoogleTakeoutJSONParser.TakeoutModel
{
    public class GooglePhotosOriginInfo
    {
        public GooglePhotosOriginInfo(WebUploadInfo webUpload)
        {
            WebUpload = webUpload;
        }
        public WebUploadInfo WebUpload { get; set; }
    }
}