from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
import requests

class SkinCareApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.file_chooser = FileChooserListView()
        analyze_button = Button(text="Analyze Face")
        analyze_button.bind(on_press=self.analyze_face)
        layout.add_widget(self.file_chooser)
        layout.add_widget(analyze_button)
        self.result_label = Label(text="Upload an image and analyze your skin")
        layout.add_widget(self.result_label)
        return layout

    def show_error(self, message):
        popup = Popup(title="Error", content=Label(text=message), size_hint=(0.8, 0.2))
        popup.open()

    def analyze_face(self, instance):
        if not self.file_chooser.selection:
            self.show_error("No file selected")
            return

        file_path = self.file_chooser.selection[0]
        try:
            url = "http://localhost:5000/analyze"
            files = {'image': open(file_path, 'rb')}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                result = response.json()
                if "error" in result:
                    self.show_error(result["error"])
                else:
                    recommendations = result.get("recommendations", [])
                    self.result_label.text = f"Recommendations: {', '.join(recommendations)}"
            else:
                self.show_error(f"Error during analysis: {response.status_code}")
        except Exception as e:
            self.show_error(f"Failed to analyze: {str(e)}")

if __name__ == '__main__':
    SkinCareApp().run()
