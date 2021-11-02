using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using System.Text.Json;


namespace AsQammServer.Models
{
    public class User
    {
        [Required]
        public int Id
        { 
            get; 
            set;
        }

        [Required]
        public short Type
        {
            get;
            set;
        }

        [Required]
        public string FilePath
        {
            get;
            set;
        }

        [Required]
        public string Login
        {
            get;
            set;
        }

        [Required]
        [StringLength(64, MinimumLength = 64)]
        public string Password
        {
            get;
            set;
        }

        [Required]
        public string Description
        {
            get;
            set;
        }
    }
}
