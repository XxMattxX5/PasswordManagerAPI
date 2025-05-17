package com.example.password_manager.ui

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.Toast
import androidx.lifecycle.lifecycleScope
import com.example.password_manager.R
import okhttp3.Call
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException
import okhttp3.Callback
import okhttp3.Response
import com.example.password_manager.BuildConfig
import com.example.password_manager.utils.AuthManager
import kotlinx.coroutines.launch


class RegisterActivity: BaseActivity() {



    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        val createAccountButton = findViewById<Button>(R.id.button3)

        createAccountButton.setOnClickListener {
            val username = findViewById<EditText>(R.id.editTextText).text.toString()
            val email = findViewById<EditText>(R.id.editTextTextEmail).text.toString()
            val password = findViewById<EditText>(R.id.editTextTextPassword).text.toString()
            val passwordConfirm = findViewById<EditText>(R.id.editTextTextPassword1).text.toString()

            registerUser(username, email, password, passwordConfirm)

        }


    }

    override fun onResume() {
        super.onResume()

        lifecycleScope.launch {
            if (AuthManager.isLogged == null) {
                val valid = AuthManager.validateToken(this@RegisterActivity)
                if (valid) {
                    navigateToPasswordList()
                }
            } else if (AuthManager.isLogged == true) {
                navigateToPasswordList()
            }
        }
    }

    private fun navigateToPasswordList() {
        val intent = Intent(this, PasswordListActivity::class.java)
        startActivity(intent)
        finish()
    }



    fun registerUser(username: String, email: String, password: String, passwordConfirm: String) {
        val createAccountButton = findViewById<Button>(R.id.button3)
        val progressBar = findViewById<ProgressBar>(R.id.progressBar)

        createAccountButton.isEnabled = false
        progressBar.visibility = View.VISIBLE

        val baseUrl = BuildConfig.BASE_URL
        val client = OkHttpClient()

        val json = JSONObject()
        json.put("username", username)
        json.put("email", email)
        json.put("password", password)
        json.put("password_confirm", passwordConfirm)

        val mediaType = "application/json; charset=utf-8".toMediaType()

        val requestBody = json.toString().toRequestBody(mediaType)

        val request = Request.Builder()
            .url("$baseUrl/auth/register/") // change this to your actual endpoint
            .post(requestBody)
            .build()

        client.newCall(request).enqueue(object : Callback {
            override fun onFailure(call: Call, e: IOException) {
                // Handle network error
                Log.e("Register", "Network error", e)
            }

            override fun onResponse(call: Call, response: Response) {
                if (response.isSuccessful) {
                    val responseBody = response.body?.string()
                    // Show success message to user
                    Handler(Looper.getMainLooper()).post {
                        progressBar.visibility = View.GONE
                        createAccountButton.isEnabled = true
                        Toast.makeText(this@RegisterActivity, "Account Created!", Toast.LENGTH_LONG)
                            .show()
                    }
                    val intent = Intent(this@RegisterActivity, LoginActivity::class.java)
                    startActivity(intent)

                    finish()

                } else {
                    val errorBody = response.body?.string()
                    val errorJson = JSONObject(errorBody ?: "{}")

                    val errors = mutableListOf<String>()

                    if (errorJson.has("username")) {
                        val msg = errorJson.getJSONArray("username").join(", ")
                        errors.add("Username: $msg")
                    }

                    if (errorJson.has("email")) {
                        val msg = errorJson.getJSONArray("email").join(", ")
                        errors.add("Email: $msg")
                    }

                    if (errorJson.has("password")) {
                        val msg = errorJson.getJSONArray("password").join(", ")
                        errors.add("Password: $msg")
                    }

                    if (errorJson.has("password_confirm")) {
                        val msg = errorJson.getJSONArray("password_confirm").join(", ")
                        errors.add("Password Confirm: $msg")
                    }

                    // Show validation errors to the user in a Toast (or any UI element you want)
                    Handler(Looper.getMainLooper()).post {
                        progressBar.visibility = View.GONE
                        createAccountButton.isEnabled = true
                        Toast.makeText(
                            this@RegisterActivity,
                            errors.joinToString("\n"),
                            Toast.LENGTH_LONG
                        ).show()
                    }
                }


            }
        })

    }

}