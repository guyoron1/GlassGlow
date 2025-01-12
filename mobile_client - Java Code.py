"""OkHttpClient client = new OkHttpClient();

File imageFile = new File("path/to/image.jpg");
RequestBody body = new MultipartBody.Builder()
    .setType(MultipartBody.FORM)
    .addFormDataPart("image", "face.jpg",
        RequestBody.create(MediaType.parse("image/jpeg"), imageFile))
    .build();

Request request = new Request.Builder()
    .url("http://your-backend-url/analyze")
    .post(body)
    .build();

Response response = client.newCall(request).execute();
String recommendations = response.body().string();"""
