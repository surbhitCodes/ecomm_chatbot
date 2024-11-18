import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'pages/queries.dart';
import 'pages/technical_support.dart';
import 'pages/project_planning.dart';
import 'styles.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Load environment variables
  try {
    await dotenv.load(fileName: ".env");
    if (kDebugMode) {
      print("Environment variables loaded successfully.");
    }
  } catch (e) {
    if (kDebugMode) {
      print("Error loading .env file: $e");
    }
  }

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Arbor Assistant',
      theme: ThemeData(primarySwatch: Colors.green),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

   @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 255, 255, 255),
      appBar: AppBar(
        title: Column(
          children: [
            Image.asset(
              'images/whitelogo.png',
              height: 40,
            ),
            const SizedBox(height: 10),
            Text("Arbor's AI Assistant", style: appBarTitleStyle),
            const SizedBox(height: 10),
          ],
        ),
        backgroundColor: const Color.fromARGB(255, 0, 120, 80),
        toolbarHeight: 100,
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              'Welcome! What brings you here?',
              style: boldTextStyle,
            ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const QueriesPage()),
                    );
                  },
                  style: buttonStyle,
                  child: const Text('General Queries'),
                ),
                const SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const TechnicalSupportPage()),
                    );
                  },
                  style: buttonStyle,
                  child: const Text('Technical Support'),
                ),
                const SizedBox(width: 20),
                ElevatedButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const ProjectPlanningPage()),
                    );
                  },
                  style: buttonStyle,
                  child: const Text('Project Planning'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}