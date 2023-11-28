import { Filesystem, Directory, Encoding } from '@capacitor/filesystem';

const writeFile = async (text: string) => {
  await Filesystem.writeFile({
    path: "secrets/text.txt",
    data: text,
    directory: Directory.Documents,
    encoding: Encoding.UTF8,
  });
};

writeFile("Capacitor is really cool!");

import { Camera, CameraResultType } from '@capacitor/camera';

const takePicture = async (element: HTMLElement) => {
  const image = await Camera.getPhoto({
    quality: 90,
    allowEditing: true,
    resultType: CameraResultType.Uri
  });

  var imageUrl = image.webPath;
  element.src = imageUrl;
};

const img = document.getElementById("my-photo");
takePicture(img);

import { Share } from '@capacitor/share';

const shareCapacitorUrl = async () => {
  await Share.share({
    title: 'Capacitor is cool!',
    text: 'Really awesome thing you need to see right meow',
    url: 'http://awdev.my.id/',
    dialogTitle: 'Share with buddies',
  });
}

shareCapacitorUrl();


