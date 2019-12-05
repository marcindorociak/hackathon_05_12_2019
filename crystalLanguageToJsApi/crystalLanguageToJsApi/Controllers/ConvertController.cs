using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using CrystalLanguageToJsDll;


namespace crystalLanguageToJsApi.Controllers
{
    public class codePost
    {
        public string code { get; set; }
    }

    [Route("api/[controller]")]
    [ApiController]
    public class ConvertController : ControllerBase
    {
        public class codePost
        {
            public string[] code { get; set; }
        }

        [HttpPost]
        public string[] Post([FromBody] codePost code)
        {
            string textToConvert = string.Join("\n\t", code.code);

            CrystalLanguageToJsDll.CrystalLanguageToJsDll convertClass = new CrystalLanguageToJsDll.CrystalLanguageToJsDll();
            textToConvert = convertClass.ConvertCodeMain(textToConvert);
            string[] lines = textToConvert.Split(
                new[] { "\r\n", "\r", "\n" },
                StringSplitOptions.None
            );

            return lines;
       
        }

    }
}