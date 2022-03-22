using System.ComponentModel;
using Wit.ViewModels;
using Xamarin.Forms;

namespace Wit.Views
{
    public partial class ItemDetailPage : ContentPage
    {
        public ItemDetailPage()
        {
            InitializeComponent();
            BindingContext = new ItemDetailViewModel();
        }
    }
}