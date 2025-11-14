import { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Pressable,
  KeyboardAvoidingView,
  Platform,
  Image,
} from "react-native";
import { styles } from "../styles/RegisterStyles";
import { router } from "expo-router";

export default function RegisterPage() {
  const [first, setFirst] = useState("");
  const [last, setLast] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [emailError, setEmailError] = useState("");
  const [passwordError, setPasswordError] = useState("");

  const validateEmail = (text: string) => {
    setEmail(text);
    const emailRegex = /\S+@\S+\.\S+/;
    if (!emailRegex.test(text)) setEmailError("Please enter a valid email address.");
    else setEmailError("");
  };

  const validatePassword = (text: string) => {
    setPassword(text);
    if (text.length < 6) setPasswordError("Password must be at least 6 characters.");
    else setPasswordError("");
  };

  const isFormValid =
    first.trim() &&
    last.trim() &&
    email.length > 0 &&
    password.length > 0 &&
    emailError === "" &&
    passwordError === "";

  return (
    <KeyboardAvoidingView
      style={styles.safe}
      behavior={Platform.OS === "ios" ? "padding" : undefined}
    >
      <View style={styles.container}>
        <View style={styles.logoRow}>
          <Image
            source={require("../assets/Vellora_Dark_Logo.png")}
            style={styles.logo}
            resizeMode="contain"
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>First Name</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter First Name"
            placeholderTextColor="#9CA3AF"
            value={first}
            onChangeText={setFirst}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Last Name</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Last Name"
            placeholderTextColor="#9CA3AF"
            value={last}
            onChangeText={setLast}
          />
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Email Address</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Email"
            placeholderTextColor="#9CA3AF"
            autoCapitalize="none"
            keyboardType="email-address"
            value={email}
            onChangeText={validateEmail}
          />
          {emailError ? (
            <Text style={{ color: "red", marginTop: 4 }}>{emailError}</Text>
          ) : null}
        </View>

        <View style={styles.fieldGroup}>
          <Text style={styles.label}>Password</Text>
          <TextInput
            style={styles.input}
            placeholder="Enter Password"
            placeholderTextColor="#9CA3AF"
            secureTextEntry
            value={password}
            onChangeText={validatePassword}
          />
          {passwordError ? (
            <Text style={{ color: "red", marginTop: 4 }}>{passwordError}</Text>
          ) : null}
        </View>

        <Pressable
          style={[styles.ctaButton, { opacity: isFormValid ? 1 : 0.4 }]}
          disabled={!isFormValid}
          onPress={() => console.log("Register user")}
        >
          <Text style={styles.ctaButtonText}>Continue</Text>
        </Pressable>

        <Text style={styles.footerText}>
          Already have an account?{" "}
          <Text
            style={styles.link}
            onPress={() => router.push("/pages/LoginPage")}
          >
            Log in
          </Text>
        </Text>
      </View>
    </KeyboardAvoidingView>
  );
}
