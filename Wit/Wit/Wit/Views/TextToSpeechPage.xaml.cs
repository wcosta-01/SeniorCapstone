using System;
using Xamarin.Forms;
using Xamarin.Essentials;
using System.Collections.Generic;
using System.Linq;

namespace Wit.Views
{
    public partial class TextToSpeechPage : ContentPage
    {
        IEnumerable<Locale> locales;
        public TextToSpeechPage()
        {
            InitializeComponent();
        }

        protected async override void OnAppearing()
        {
            base.OnAppearing();

            locales = await TextToSpeech.GetLocalesAsync();

            foreach (var l in locales)
                Languages.Items.Add(l.Name);
        }

        void Button_Clicked(object sender, EventArgs e)
        {
            if (Languages.SelectedIndex > 0)
            {
                TextToSpeech.SpeakAsync(TextToSpeak.Text, new
                    SpeechOptions
                {
                    Locale = locales.Single(l => l.Name == 
                    Languages.SelectedItem.ToString())
                });
            }
        }
    }
}