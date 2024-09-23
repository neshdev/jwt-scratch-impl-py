using System.Data.SqlTypes;
using System.Runtime.Intrinsics.Arm;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace neshdev;



public class ConsoleApp
{
    public static int Main(string[] args)
    {
        Console.WriteLine("Creating a JWT");
        var header = new Header
        {
            Alg = "RS256",
            Typ = "JWT",
        };

        var payload = new Payload {
            Sub = "1234567890",
            Name = "John Doe",
            Admin = true,
            Iat = 1516239022,
        };
        var result = Jwt.Encode(header, payload);
        var arr = result.Split(".");
        Console.WriteLine(arr[0] == "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9");
        Console.WriteLine(arr[0]);
        Console.WriteLine(arr[1] == "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0");
        Console.WriteLine(arr[1]);
        Console.WriteLine(arr[2] == "c2S8PX0vOe8yn51usQBlO-6f5SGaIdbilq94Zpyezv_BCfV4oVo_IxWEoNoz9gsdmd17MtwG3FqBto-eubn0lJy9Pf4u_eXCginnpoaUkIjCKcxBvIpRt7_Zin1f2BDGPxa_ow4DuBamlpsILV8hyf6uJStd0L-0gcrfkwbWca8ohFSKA-Pckufrw_-Nf38jJgflUPmsi3e7U8JC28vuwiF6bzPiR4l3gS3h7qAth8UVPBhA3xKOGI4kYdzvmh5M1NzeG916iB82-xH6PyDYDAwmW836k-1Y8GycN7Ep4-T-BPRRZI7aSfZRIe7ENVBQ974MoT1u2963afoBG_LT-w");
        Console.WriteLine(arr[2]);
        return 0;
    }
}


public class Jwt
{
    Jwt()
    {

    }

    public static string Encode(Header header, Payload payload)
    {
        var h = Helpers.Encode(header);
        var p = Helpers.Encode(payload);
        var c = $"{h}.{p}";
        var s = Helpers.Sign(c);
        return $"{h}.{p}.{s}";
    }
}

public static class Helpers
{

    public static string UrlSafeB64Encode(byte[] arr)
    {
        var e = Convert
            .ToBase64String(arr, Base64FormattingOptions.None)
            .Replace("=", "")
            .Replace('+', '-')
            .Replace('/', '_');
        return e;
    }
    public static string Encode<T>(T message)
    {
        var payload = JsonSerializer.SerializeToUtf8Bytes(message, options: new JsonSerializerOptions
        {
            PropertyNamingPolicy = JsonNamingPolicy.CamelCase
        });
        var encoded = UrlSafeB64Encode(payload);
        var bytesUtf8 = Encoding.UTF8.GetBytes(encoded);
        var strUtf8 = Encoding.UTF8.GetString(bytesUtf8);
        return strUtf8;
    }

    public static string Sign(string data){
        var key = RSA.Create();
        key.ImportFromPem("-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAwhvqCC+37A+UXgcvDl+7nbVjDI3QErdZBkI1VypVBMkKKWHM\nNLMdHk0bIKL+1aDYTRRsCKBy9ZmSSX1pwQlO/3+gRs/MWG27gdRNtf57uLk1+lQI\n6hBDozuyBR0YayQDIx6VsmpBn3Y8LS13p4pTBvirlsdX+jXrbOEaQphn0OdQo0WD\noOwwsPCNCKoIMbUOtUCowvjesFXlWkwG1zeMzlD1aDDS478PDZdckPjT96ICzqe4\nO1Ok6fRGnor2UTmuPy0f1tI0F7Ol5DHAD6pZbkhB70aTBuWDGLDR0iLenzyQecmD\n4aU19r1XC9AHsVbQzxHrP8FveZGlV/nJOBJwFwIDAQABAoIBAFCVFBA39yvJv/dV\nFiTqe1HahnckvFe4w/2EKO65xTfKWiyZzBOotBLrQbLH1/FJ5+H/82WVboQlMATQ\nSsH3olMRYbFj/NpNG8WnJGfEcQpb4Vu93UGGZP3z/1B+Jq/78E15Gf5KfFm91PeQ\nY5crJpLDU0CyGwTls4ms3aD98kNXuxhCGVbje5lCARizNKfm/+2qsnTYfKnAzN+n\nnm0WCjcHmvGYO8kGHWbFWMWvIlkoZ5YubSX2raNeg+YdMJUHz2ej1ocfW0A8/tmL\nwtFoBSuBe1Z2ykhX4t6mRHp0airhyc+MO0bIlW61vU/cPGPos16PoS7/V08S7ZED\nX64rkyECgYEA4iqeJZqny/PjOcYRuVOHBU9nEbsr2VJIf34/I9hta/mRq8hPxOdD\n/7ES/ZTZynTMnOdKht19Fi73Sf28NYE83y5WjGJV/JNj5uq2mLR7t2R0ZV8uK8tU\n4RR6b2bHBbhVLXZ9gqWtu9bWtsxWOkG1bs0iONgD3k5oZCXp+IWuklECgYEA27bA\n7UW+iBeB/2z4x1p/0wY+whBOtIUiZy6YCAOv/HtqppsUJM+W9GeaiMpPHlwDUWxr\n4xr6GbJSHrspkMtkX5bL9e7+9zBguqG5SiQVIzuues9Jio3ZHG1N2aNrr87+wMiB\nxX6Cyi0x1asmsmIBO7MdP/tSNB2ebr8qM6/6mecCgYBA82ZJfFm1+8uEuvo6E9/R\nyZTbBbq5BaVmX9Y4MB50hM6t26/050mi87J1err1Jofgg5fmlVMn/MLtz92uK/hU\nS9V1KYRyLc3h8gQQZLym1UWMG0KCNzmgDiZ/Oa/sV5y2mrG+xF/ZcwBkrNgSkO5O\n7MBoPLkXrcLTCARiZ9nTkQKBgQCsaBGnnkzOObQWnIny1L7s9j+UxHseCEJguR0v\nXMVh1+5uYc5CvGp1yj5nDGldJ1KrN+rIwMh0FYt+9dq99fwDTi8qAqoridi9Wl4t\nIXc8uH5HfBT3FivBtLucBjJgOIuK90ttj8JNp30tbynkXCcfk4NmS23L21oRCQyy\nlmqNDQKBgQDRvzEB26isJBr7/fwS0QbuIlgzEZ9T3ZkrGTFQNfUJZWcUllYI0ptv\ny7ShHOqyvjsC3LPrKGyEjeufaM5J8EFrqwtx6UB/tkGJ2bmd1YwOWFHvfHgHCZLP\n34ZNURCvxRV9ZojS1zmDRBJrSo7+/K0t28hXbiaTOjJA18XAyyWmGg==\n-----END RSA PRIVATE KEY-----\n");

        using (var sha256 = SHA256.Create()) {
            var bytes = Encoding.UTF8.GetBytes(data);
            var hash = sha256.ComputeHash(bytes);
            var sign = key.SignHash(hash, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
            var encoded = Helpers.UrlSafeB64Encode(sign);
            var bytesUtf8 = Encoding.UTF8.GetBytes(encoded);
            var strUtf8 = Encoding.UTF8.GetString(bytesUtf8);
            return strUtf8; 
        }
    }
}

public class Header
{
    public required string Alg { get; set; }
    public required string Typ { get; set; }
}

public class Payload
{
    public string Sub { get; set; }
    public string Name { get; set; }
    public bool Admin { get; set; }
    public int Iat { get; set; }

}
