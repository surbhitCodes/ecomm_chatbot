import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import '../styles.dart'; // Import styles.dart for reusable styles

class TechnicalSupportPage extends StatefulWidget {
  const TechnicalSupportPage({super.key});

  @override
  // ignore: library_private_types_in_public_api
  _TechnicalSupportPageState createState() => _TechnicalSupportPageState();
}

class _TechnicalSupportPageState extends State<TechnicalSupportPage> {
  final TextEditingController _queryController = TextEditingController();
  // ignore: unused_field, prefer_final_fields
  String _response = '';
  // ignore: prefer_final_fields
  List<String> _conversation = [];

  final String baseUrl = dotenv.env['BASE_URL'] ?? 'http://localhost:8000';
  final String apiKey = dotenv.env['API_KEY'] ?? '';

  Future<void> sendTechnicalSupportQuery() async {
    String query = _queryController.text.trim();
    if (query.isEmpty) {
      setState(() {
        _conversation.add('Please enter your query ...');
      });
      return;
    }

    try {
      final response = await http.post(
        Uri.parse('$baseUrl/technical-support'),
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
        },
        body: jsonEncode({'question': query}),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _conversation.add('You: $query');
          _conversation.add('Assistant: ${data['answer']}');
        });
      } else {
        setState(() {
          _conversation.add(
              'Assistant: Error ${response.statusCode} - ${response.body}');
        });
      }
    } catch (e) {
      setState(() {
        _conversation.add('Assistant: An error occurred: $e');
      });
    } finally {
      _queryController.clear();
    }
  }

  @override
  void dispose() {
    _queryController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Technical Support', style: appBarTitleStyle),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisSize: MainAxisSize.max,
          children: [
            // Conversation View
            Expanded(
              child: ListView.builder(
                itemCount: _conversation.length,
                itemBuilder: (context, index) {
                  bool isUser = index % 2 == 0;
                  return Align(
                    alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                    child: Container(
                      padding: const EdgeInsets.all(10),
                      margin: const EdgeInsets.symmetric(vertical: 5),
                      decoration: BoxDecoration(
                        color: isUser ? Colors.blueAccent.shade100 : Colors.grey.shade300,
                        borderRadius: BorderRadius.circular(10),
                      ),
                      child: Text(
                        _conversation[index],
                        style: normalTextStyle.copyWith(
                          color: isUser ? Colors.white : Colors.black,
                        ),
                      ),
                    ),
                  );
                },
              ),
            ),
            const Divider(),
            // Input Field
            TextField(
              controller: _queryController,
              decoration: const InputDecoration(
                labelText: 'Enter your technical support query',
                border: OutlineInputBorder(),
              ),
              onSubmitted: (_) => sendTechnicalSupportQuery(),
            ),
            const SizedBox(height: 10),
            // Send Button
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: sendTechnicalSupportQuery,
                style: buttonStyle,
                child: const Text('Send Query'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
