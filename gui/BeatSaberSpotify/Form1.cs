﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.Remoting.Channels;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using DotNetEnv;


namespace BeatSaberSpotify
{
    public partial class Form1 : Form
    {
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

            if (btnStart.Text == "Start")
            {
                btnStart.Text = "Stop";
                txtOutput.Text = "";
                pythonRun.RunWorkerAsync();
            }
            else
            {
                pythonRun.CancelAsync();
                btnStart.Text = "Start";
                
                    
            }
                



        }

        private void BackgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            pythonRun.WorkerSupportsCancellation = true;
            //All the secret stuff is stored in .env file WHICH YOU CANT HAVE!
            //If you are building from source, you can delete the next line
            DotNetEnv.Env.Load();
            //Get all stuf
            string path = txtPath.Text;
            string uri = txtURI.Text;
            string username = txtUser.Text;
            string headsetType = "";
            string model = "";
            txtHeadset.Invoke(new MethodInvoker(delegate { headsetType = txtHeadset.Text; }));
            txtVersion.Invoke(new MethodInvoker(delegate { model = txtVersion.Text; }));
            //If you are building from source, replace these with your client and secret id
            string client_id = Environment.GetEnvironmentVariable("SPOTIPY-CLIENT-ID");
            string secret_id = Environment.GetEnvironmentVariable("SPOTIPY-SECRET-ID");
            //Runs the program from a local directory
            string directory = Path.GetDirectoryName(Application.ExecutablePath);
            string python_folder = @"python/run.py";
            string python_directory = Path.Combine(directory, python_folder);
            //Parse arguements to an array
   
            string[] args = { path, uri, username, client_id, secret_id, headsetType, model };
            //RUN IT!
            if (File.Exists(python_directory))
            {
                run_cmd(python_directory, args, sender);
                progress.Invoke(new MethodInvoker(delegate { progress.Value = 0; }));
                btnStart.Invoke(new MethodInvoker(delegate { btnStart.Text = "Start"; }));
                return;
            }
            else
            {
                txtOutput.Invoke(new MethodInvoker(delegate { txtOutput.Text = "Cannot find python executable. Are you sure you downloaded everything?"; }));
                progress.Invoke(new MethodInvoker(delegate { progress.Value = 0; }));
                btnStart.Invoke(new MethodInvoker(delegate { btnStart.Text = "Start"; }));
                return;
            }
        }
        public string getDirectory(){
            string pythonPath = string.Format(@"C:\Users\{0}\AppData\Local\Programs\Python\", Environment.UserName);
            var list = new List<string>();
            foreach (string directory in Directory.GetDirectories(pythonPath))
            {
                list.Add(directory);

            }
            return (list.Max() + @"\python.exe");   
        }
        public void run_cmd(string cmd, string[] args, object sender)
        {
            
            //Create process, and change settings
            Process process = new Process();
            process.StartInfo.FileName = "python.exe";
            process.StartInfo.Arguments = string.Format("\"{0}\" \"{1}\" \"{2}\" \"{3}\" \"{4}\" \"{5}\" \"{6}\" \"{6}\"", cmd, args[0], args[1], args[2], args[3], args[4], args[5], args[6], args[7]);
            process.StartInfo.UseShellExecute = false;// Do not use OS shell
            process.StartInfo.CreateNoWindow = true; // We don't need new window
            process.StartInfo.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            process.StartInfo.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)            process.ErrorDataReceived += cmd_Error;
            process.OutputDataReceived += cmd_DataReceived;
            process.EnableRaisingEvents = true;
            try {
                process.Start();
            }
            catch (Win32Exception){
                process.StartInfo.FileName = getDirectory();
                process.Start();
            }
            
            //recieve data asyncronously, others program looks like it is hanging
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();
            
            
            
            while (true) 
            {
                Process[] pname = Process.GetProcessesByName("python");
                if (pname.Length == 0)
                {
                    return;
                }

                if ((sender as BackgroundWorker).CancellationPending == true)
                {
                    foreach (var processToKill in pname)
                    {
                        processToKill.Kill();
                    }

                    return;
                }
                Thread.Sleep(500);
            }
            
        }

        private void cmd_DataReceived(object sender, DataReceivedEventArgs e)
        {
            string line = e.Data;
            //Stop Errors
            if (line != null) { 
            if (line.Contains("Total"))
                {
                    //Basically sets up the progress bar for the maximum amount of songs
                    string replaced = line.Replace("Total", "");
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
                        string replaced = line.Replace("Current", "");
                        int current = int.Parse(replaced);
                        progress.Invoke(new MethodInvoker(delegate { progress.Value = current; }));
                    }
                    else
                    {
                        //Logging
                        if (line != null)
                        {
                            if (line == "Error has occured! Check log for more details")
                            {
                                progress.Invoke(new MethodInvoker(delegate { progress.Value = 0; }));
                                btnStart.Invoke(new MethodInvoker(delegate { btnStart.Text = "Start"; }));

                            }
                            txtOutput.Invoke(new MethodInvoker(delegate { txtOutput.AppendText(line); txtOutput.AppendText(Environment.NewLine); }));
                        }


                    }
                }
            }
        }

        private void cmd_Error(object sender, DataReceivedEventArgs e)
        {
            //Similar stuff, just without logging stuff
            string line = e.Data;
            if (line != null)
            {
                txtOutput.Invoke(new MethodInvoker(delegate { txtOutput.AppendText(line); txtOutput.AppendText(Environment.NewLine); }));
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
        private void Form1_FormClosed(object sender, FormClosedEventArgs e){
            
            Process[] pname = Process.GetProcessesByName("python");
            foreach (var processToKill in pname)
            {
                processToKill.Kill();
            }

        }

        private void button1_Click(object sender, EventArgs e)
        {
            System.Diagnostics.Process.Start("https://beatsage.com/#user-content-what-is-the-difference-between-v2-and-v2-flow");

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
