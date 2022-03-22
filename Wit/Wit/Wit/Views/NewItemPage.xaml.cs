using System;
using System.Collections.Generic;
using System.ComponentModel;
using Wit.Models;
using Wit.ViewModels;
using Xamarin.Forms;
using Xamarin.Forms.Xaml;

namespace Wit.Views
{
    public partial class NewItemPage : ContentPage
    {
        public Item Item { get; set; }

        public NewItemPage()
        {
            InitializeComponent();
            BindingContext = new NewItemViewModel();
        }
    }
}