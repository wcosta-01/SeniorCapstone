using System;
using System.Collections.Generic;
using System.Text;
using System.Windows.Input;
using Xamarin.Essentials;
using Xamarin.Forms;

namespace Wit.ViewModels
{
    public class TranslatingViewModel : BaseViewModel
    {
        public TranslatingViewModel()
        {
            Title = "Translate";
        }
        public ICommand ToTranslateCommand { get; }
    }
}
