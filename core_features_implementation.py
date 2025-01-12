from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView

"This part (first code block) handles the user interface"
"for uploading the image and triggering the face analysis"
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
import requests


class SkinCareApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView()
        analyze_button = Button(text="Analyze Face")
        analyze_button.bind(on_press=self.analyze_face)
        layout.add_widget(file_chooser)
        layout.add_widget(analyze_button)
        self.file_chooser = file_chooser
        return layout

    def analyze_face(self, instance):
        file_path = self.file_chooser.selection[0]  # Get the selected file path
        print(f"Analyzing face from {file_path}...")

        # Send the image to backend for analysis
        url = "http://localhost:5000/analyze"
        files = {'image': open(file_path, 'rb')}
        response = requests.post(url, files=files)

        if response.status_code == 200:
            print("Skin care recommendations:", response.json())
        else:
            print("Error during analysis")


if __name__ == '__main__':
    SkinCareApp().run()
