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

            if (browser.ShowDialog() == DialogResult.OK)
            {
                txtPath.Text = browser.SelectedPath;
            }
        }

        private void BtnStart_Click(object sender, EventArgs e)
        {
            try
            {
                pythonRun.RunWorkerAsync();
                if (progress.Value == progress.Maximum)
                {
                    progress.Value = 0;
                }
            }
            catch
            {
                Console.WriteLine("stop pressing the button you banana");
            }



        }

        public string run_cmd(string cmd, string[] args)
        {
            //string result = "";
            Process process = new Process();
            process.StartInfo.FileName = "python.exe";
            process.StartInfo.Arguments = string.Format("\"{0}\" \"{1}\" \"{2}\" \"{3}\"", cmd, args[0], args[1], args[2]);
            process.StartInfo.UseShellExecute = false;// Do not use OS shell
            process.StartInfo.CreateNoWindow = true; // We don't need new window
            process.StartInfo.RedirectStandardOutput = true;// Any output, generated by application will be redirected back
            process.StartInfo.RedirectStandardError = true; // Any error in standard output will be redirected back (for example exceptions)
            process.Start();

            StreamReader reader = process.StandardOutput;
            StringBuilder builder = new StringBuilder();

            string line;
            while ((line = reader.ReadLine()) != null)
            {
                if (line.Contains("Total"))
                {
                    string replaced = line.Replace("Total", " ");
                    int total = int.Parse(replaced);
                    progress.Invoke(new MethodInvoker(delegate { progress.Maximum = total; }));
                }
                else
                {
                    if (line.Contains("Current"))
                    {
                        string replaced = line.Replace("Current", " ");
                        int current = int.Parse(replaced);
                        progress.Invoke(new MethodInvoker(delegate { progress.Value = current; }));
                    }
                    else
                    {
                        builder.AppendLine(line);
                        txtOutput.Invoke(new MethodInvoker(delegate { txtOutput.AppendText(line); txtOutput.AppendText(Environment.NewLine); }));
                        Console.WriteLine(line);
                    }

                }

            }

            string allLines = builder.ToString();

            return allLines;

        }
        private void TxtOutput_TextChanged(object sender, EventArgs e)
        {
            txtOutput.SelectionStart = txtOutput.Text.Length;
            txtOutput.ScrollToCaret();
        }

        private void BackgroundWorker1_DoWork(object sender, DoWorkEventArgs e)
        {
            string path = txtPath.Text;
            string uri = txtURI.Text;
            string username = txtUser.Text;
            string directory = Path.GetDirectoryName(Application.ExecutablePath);
            string python_folder = @"python/run.py";
            string python_directory = Path.Combine(directory, python_folder);
            txtOutput.Text = python_directory;
            string pathTest = @"C:/Users/mcdougalls/OneDrive - Wesley College/test.py";
            string[] args = { path, uri, username };
            string output = run_cmd(python_directory, args);
            


        }

        private void BtnHe_Click(object sender, EventArgs e)
        {
            Process.Start("https://github.com/MartyMcKnife/BeatSaberSpotify/wiki");
        }
    }
}
//Archive

/*
           
           */
