﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using DotNetEnv;


namespace BeatSaberSpotify
{
    public partial class Form1 : Form
    {
        bool createFile = true;
        public Form1()
        {
            InitializeComponent();
        }

        private void Label1_Click(object sender, EventArgs e)
        {

        }

        private void Button2_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("https://github.com/MartyMcKnife/BeatSaberSpotify/wiki");
        }

        private void TextBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void BtnExplore_Click(object sender, EventArgs e)
        {
            //File Explorer - Gets path selected, and stores it to text box

            if (browser.ShowDialog() == DialogResult.OK)
            {
                txtPath.Text = browser.SelectedPath;
            }
        }

        private void BtnStart_Click(object sender, EventArgs e)
        {
            //Starts the program, and starts the progressbar
            try
            {
                createFile = true;
                pythonRun.RunWorkerAsync();
                if (progress.Value == progress.Maximum)
                {
                    progress.Value = 0;
                }
            }
            //10/10 Error catching
            catch
            {
                Console.WriteLine("stop pressing the button you banana");
            }



        }

        private void BackgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            //All the secret stuff is stored in .env file WHICH YOU CANT HAVE!
            //If you are building from source, you can delete the next line
            DotNetEnv.Env.Load();
            //Get all stuf
            string path = txtPath.Text;
            string uri = txtURI.Text;
            string username = txtUser.Text;
            //If you are building from source, replace these with your client and secret id
            string client_id = Environment.GetEnvironmentVariable("SPOTIPY-CLIENT-ID");
            string secret_id = Environment.GetEnvironmentVariable("SPOTIPY -SECRET-ID");
            //Runs the program from a local directory
            string directory = Path.GetDirectoryName(Application.ExecutablePath);
            string python_folder = @"python/run.py";
            string python_directory = Path.Combine(directory, python_folder);
            //Parse arguements to an array
            string[] args = { path, uri, username, client_id, secret_id };
            //RUN IT!
            run_cmd(python_directory, args);



        }

        public void run_cmd(string cmd, string[] args)
        {
            createFile = false;
            //Create process, and change settings
            Process process = new Process();
            process.StartInfo.FileName = "python.exe";
            process.StartInfo.Arguments = string.Format("\"{0}\" \"{1}\" \"{2}\" \"{3}\" \"{4}\" \"{5}\"", cmd, args[0], args[1], args[2], args[3], args[4]);
            process.StartInfo.UseShellExecute = false;// Do not use OS shell
            process.StartInfo.CreateNoWindow = true; // We don't need new window
            process.StartInfo.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            process.StartInfo.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)
           //No idea how this works, but it works
            process.ErrorDataReceived += cmd_Error;
            process.OutputDataReceived += cmd_DataReceived;
            process.EnableRaisingEvents = true;

            process.Start();
            //recieve data asyncronously, others program looks like it is hanging
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();


            process.WaitForExit();

   

        }

        private void cmd_DataReceived(object sender, DataReceivedEventArgs e)
        {
            string line = e.Data;
            //Stop Errors
            if (line != null) { 
            if (line.Contains("Total"))
                {
                    //Basically sets up the progress bar for the maximum amount of songs
                    string replaced = line.Replace("Total", " ");
                    try
                    {
                        int total = int.Parse(replaced);
                        progress.Invoke(new MethodInvoker(delegate { progress.Maximum = total; }));
                    }
                    catch
                    {
                        Console.WriteLine("Something funky happened");
                        Console.WriteLine(replaced);
                    }
                    
                }
                else
                {
                    //Current song it is up to
                    if (line.Contains("Current"))
                    {
                        string replaced = line.Replace("Current", " ");
                        int current = int.Parse(replaced);
                        progress.Invoke(new MethodInvoker(delegate { progress.Value = current; }));
                    }
                    else
                    {
                        //Logging
                        txtOutput.Invoke(new MethodInvoker(delegate { txtOutput.AppendText(line); txtOutput.AppendText(Environment.NewLine); }));
                        string directory = Path.Combine(Path.GetDirectoryName(Application.ExecutablePath), "beatsaverspotify.log");
                        logStuff(directory, line);


                    }
                }
            }
        }

        private void cmd_Error(object sender, DataReceivedEventArgs e)
        {
            //Similar stuff, just without logging stuff
            string line = e.Data;
            string directory = Path.Combine(Path.GetDirectoryName(Application.ExecutablePath), "beatsaverspotify.log");
            if (line != null) {
            txtOutput.Invoke(new MethodInvoker(delegate { txtOutput.AppendText(line); txtOutput.AppendText(Environment.NewLine); }));
                logStuff(directory, line);

            }
        }

        private void logStuff(string directory, string line)
        {
            //Fairly obvious what this does
            if (!File.Exists(directory) || createFile == true)
            {
                using (StreamWriter sw = File.CreateText(directory))
                {
                    sw.WriteLine("Creating Log File");
                }
            }
            using (StreamWriter sw = File.AppendText(directory))
            {
                sw.WriteLine(line);
            }
        }
        private void TxtOutput_TextChanged(object sender, EventArgs e)
        {
            //Auto scroll to bottom for text box
            txtOutput.SelectionStart = txtOutput.Text.Length;
            txtOutput.ScrollToCaret();
        }

        

        private void BtnHe_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("https://github.com/MartyMcKnife/BeatSaberSpotify/wiki");
        }

        private void Browser_HelpRequest(object sender, EventArgs e)
        {

        }
    }
}
//Archive

/*
           
           */
