import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

// normal text
final TextStyle normalTextStyle = GoogleFonts.lora(
  fontSize: 18,
);

// bold style text
final TextStyle boldTextStyle = GoogleFonts.lora(
  fontSize: 18,
  fontWeight: FontWeight.bold,
);

// app bar style
final TextStyle appBarTitleStyle = GoogleFonts.lora(
  fontSize: 20,
  fontWeight: FontWeight.bold,
  color: Colors.white,
);

// button style text
final ButtonStyle buttonStyle = ElevatedButton.styleFrom(
  textStyle: GoogleFonts.lora(fontSize: 16),
  backgroundColor: const Color.fromARGB(255, 0, 120, 80),
  foregroundColor: Colors.white
);
