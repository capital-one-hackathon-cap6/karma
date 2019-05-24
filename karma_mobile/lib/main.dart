import 'dart:async';
import 'package:flutter/material.dart';
import 'package:camera/camera.dart';

List<CameraDescription> cameras;

Future<void> main() async {
  cameras = await availableCameras();
  runApp(CameraApp());
}

class CameraApp extends StatefulWidget {
  @override
  _CameraAppState createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  CameraController controller;

  @override
  void initState() {
    super.initState();
    controller = CameraController(cameras[0], ResolutionPreset.medium);
    controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    });
  }

  @override
  void dispose() {
    controller?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    var size = 100.0;
    if (!controller.value.isInitialized) {
      return Container();
    }
    return Stack(
      children: <Widget>[
        new Container(
          child: new CustomPaint(
            foregroundPainter: new GuidelinePainter(),
            child: CameraPreview(controller),
          ),
        ),
        // new Container(
        //   child: new GestureDetector(
        //     onTap: (){
        //       print("Tap");
        //     },
        //   )
        // )
      ]
    );
  }
}

class GuidelinePainter extends CustomPainter {
  @override
  void paint(Canvas canvas, Size size) {
    Paint paint = new Paint()
      ..strokeWidth = 3.0
      ..color = Colors.green
      ..style = PaintingStyle.stroke;

    var margin = 25;

    var width = size.width - margin;
    var height = width/1.586;

    var rect = Rect.fromLTWH((size.width - width)/2, (size.height - height)/2, width, height);
    canvas.drawRect(rect, paint);
  }

  @override
  bool shouldRepaint(CustomPainter oldDelegate) => true;
}