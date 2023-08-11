
using System;
using System.Globalization;
using Xunit;
using Xunit.Sdk;


namespace GoogleTakeoutJSONParser.Test
{
    
    public class UnitTest1
    {
        [Fact]
        public void Test1()
        {
            throw new XunitException("Not Implemented");
        }

        [Fact]
        public void PhotoTakenTimeTimestamp(){

            // Arrange
            string path = @"TestData\2015-10-15 18.34.37-1.jpg.json";
            GoogleTakeoutJSONParser parser = new(path);

            // Act
            DateTime actual;
            
            
            actual = parser.GetTakenDateTime();
            

            // Assert

            DateTime actualDateTimeUtc = actual.ToUniversalTime(); // Convertir a UTC
            CultureInfo culture = new("es-ES"); // Español

            string formattedDate = actualDateTimeUtc.ToString("dd MMM yyyy, HH:mm:ss 'UTC'", culture);

            Assert.Equal(parser.TakeoutData.PhotoTakenTime.Formatted,formattedDate);


        }
    }

}

