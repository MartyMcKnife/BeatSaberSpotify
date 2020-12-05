namespace BeatSaberSpotify
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.lblPath = new System.Windows.Forms.Label();
            this.txtPath = new System.Windows.Forms.TextBox();
            this.btnExplore = new System.Windows.Forms.Button();
            this.btnHelp = new System.Windows.Forms.Button();
            this.txtURI = new System.Windows.Forms.TextBox();
            this.lblURI = new System.Windows.Forms.Label();
            this.txtUser = new System.Windows.Forms.TextBox();
            this.lblUser = new System.Windows.Forms.Label();
            this.txtOutput = new System.Windows.Forms.TextBox();
            this.btnStart = new System.Windows.Forms.Button();
            this.browser = new System.Windows.Forms.FolderBrowserDialog();
            this.pythonRun = new System.ComponentModel.BackgroundWorker();
            this.progress = new System.Windows.Forms.ProgressBar();
            this.btnHe = new System.Windows.Forms.Button();
            this.txtHeadset = new System.Windows.Forms.ComboBox();
            this.lblHeadset = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // lblPath
            // 
            this.lblPath.AutoSize = true;
            this.lblPath.Location = new System.Drawing.Point(19, 19);
            this.lblPath.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblPath.Name = "lblPath";
            this.lblPath.Size = new System.Drawing.Size(97, 13);
            this.lblPath.TabIndex = 0;
            this.lblPath.Text = "Path to Beat Saber";
            // 
            // txtPath
            // 
            this.txtPath.Location = new System.Drawing.Point(126, 17);
            this.txtPath.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.txtPath.Name = "txtPath";
            this.txtPath.Size = new System.Drawing.Size(173, 20);
            this.txtPath.TabIndex = 1;
            // 
            // btnExplore
            // 
            this.btnExplore.Location = new System.Drawing.Point(302, 16);
            this.btnExplore.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.btnExplore.Name = "btnExplore";
            this.btnExplore.Size = new System.Drawing.Size(27, 19);
            this.btnExplore.TabIndex = 2;
            this.btnExplore.Text = "...";
            this.btnExplore.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            this.btnExplore.UseVisualStyleBackColor = true;
            this.btnExplore.Click += new System.EventHandler(this.BtnExplore_Click);
            // 
            // btnHelp
            // 
            this.btnHelp.Location = new System.Drawing.Point(302, 43);
            this.btnHelp.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.btnHelp.Name = "btnHelp";
            this.btnHelp.Size = new System.Drawing.Size(27, 19);
            this.btnHelp.TabIndex = 5;
            this.btnHelp.Text = "?";
            this.btnHelp.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            this.btnHelp.UseVisualStyleBackColor = true;
            this.btnHelp.Click += new System.EventHandler(this.Button2_Click);
            // 
            // txtURI
            // 
            this.txtURI.Location = new System.Drawing.Point(126, 44);
            this.txtURI.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.txtURI.Name = "txtURI";
            this.txtURI.Size = new System.Drawing.Size(173, 20);
            this.txtURI.TabIndex = 4;
            this.txtURI.TextChanged += new System.EventHandler(this.TextBox2_TextChanged);
            // 
            // lblURI
            // 
            this.lblURI.AutoSize = true;
            this.lblURI.Location = new System.Drawing.Point(19, 45);
            this.lblURI.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblURI.Name = "lblURI";
            this.lblURI.Size = new System.Drawing.Size(61, 13);
            this.lblURI.TabIndex = 3;
            this.lblURI.Text = "Spotify URI";
            this.lblURI.Click += new System.EventHandler(this.Label1_Click);
            // 
            // txtUser
            // 
            this.txtUser.Location = new System.Drawing.Point(126, 71);
            this.txtUser.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.txtUser.Name = "txtUser";
            this.txtUser.Size = new System.Drawing.Size(173, 20);
            this.txtUser.TabIndex = 7;
            // 
            // lblUser
            // 
            this.lblUser.AutoSize = true;
            this.lblUser.Location = new System.Drawing.Point(19, 73);
            this.lblUser.Margin = new System.Windows.Forms.Padding(2, 0, 2, 0);
            this.lblUser.Name = "lblUser";
            this.lblUser.Size = new System.Drawing.Size(55, 13);
            this.lblUser.TabIndex = 6;
            this.lblUser.Text = "Username";
            // 
            // txtOutput
            // 
            this.txtOutput.Location = new System.Drawing.Point(130, 142);
            this.txtOutput.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.txtOutput.Multiline = true;
            this.txtOutput.Name = "txtOutput";
            this.txtOutput.ReadOnly = true;
            this.txtOutput.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtOutput.Size = new System.Drawing.Size(199, 64);
            this.txtOutput.TabIndex = 8;
            this.txtOutput.TextChanged += new System.EventHandler(this.TxtOutput_TextChanged);
            // 
            // btnStart
            // 
            this.btnStart.Location = new System.Drawing.Point(22, 142);
            this.btnStart.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.btnStart.Name = "btnStart";
            this.btnStart.Size = new System.Drawing.Size(84, 27);
            this.btnStart.TabIndex = 9;
            this.btnStart.Text = "Start";
            this.btnStart.UseVisualStyleBackColor = true;
            this.btnStart.Click += new System.EventHandler(this.BtnStart_Click);
            // 
            // browser
            // 
            this.browser.SelectedPath = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Beat Saber";
            this.browser.HelpRequest += new System.EventHandler(this.Browser_HelpRequest);
            // 
            // pythonRun
            // 
            this.pythonRun.DoWork += new System.ComponentModel.DoWorkEventHandler(this.BackgroundWorker1_DoWork);
            // 
            // progress
            // 
            this.progress.Location = new System.Drawing.Point(22, 123);
            this.progress.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.progress.Name = "progress";
            this.progress.Size = new System.Drawing.Size(302, 15);
            this.progress.TabIndex = 10;
            // 
            // btnHe
            // 
            this.btnHe.Location = new System.Drawing.Point(22, 180);
            this.btnHe.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.btnHe.Name = "btnHe";
            this.btnHe.Size = new System.Drawing.Size(84, 26);
            this.btnHe.TabIndex = 11;
            this.btnHe.Text = "Help";
            this.btnHe.UseVisualStyleBackColor = true;
            this.btnHe.Click += new System.EventHandler(this.BtnHe_Click);
            // 
            // txtHeadset
            // 
            this.txtHeadset.FormattingEnabled = true;
            this.txtHeadset.Items.AddRange(new object[] {
            "HTC Vive",
            "Vive Cosmos",
            "Oculus Rift/Rift S",
            "Oculus Quest/Quest 2",
            "Valve Index",
            "HP Reverb",
            "Other"});
            this.txtHeadset.Location = new System.Drawing.Point(126, 97);
            this.txtHeadset.Name = "txtHeadset";
            this.txtHeadset.Size = new System.Drawing.Size(173, 21);
            this.txtHeadset.TabIndex = 12;
            // 
            // lblHeadset
            // 
            this.lblHeadset.AutoSize = true;
            this.lblHeadset.Location = new System.Drawing.Point(22, 97);
            this.lblHeadset.Name = "lblHeadset";
            this.lblHeadset.Size = new System.Drawing.Size(74, 13);
            this.lblHeadset.TabIndex = 13;
            this.lblHeadset.Text = "Headset Type";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(340, 224);
            this.Controls.Add(this.lblHeadset);
            this.Controls.Add(this.txtHeadset);
            this.Controls.Add(this.btnHe);
            this.Controls.Add(this.progress);
            this.Controls.Add(this.btnStart);
            this.Controls.Add(this.txtOutput);
            this.Controls.Add(this.txtUser);
            this.Controls.Add(this.lblUser);
            this.Controls.Add(this.btnHelp);
            this.Controls.Add(this.txtURI);
            this.Controls.Add(this.lblURI);
            this.Controls.Add(this.btnExplore);
            this.Controls.Add(this.txtPath);
            this.Controls.Add(this.lblPath);
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Margin = new System.Windows.Forms.Padding(2, 2, 2, 2);
            this.Name = "Form1";
            this.Text = "BeatSaberSpotify";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label lblPath;
        private System.Windows.Forms.TextBox txtPath;
        private System.Windows.Forms.Button btnExplore;
        private System.Windows.Forms.Button btnHelp;
        private System.Windows.Forms.TextBox txtURI;
        private System.Windows.Forms.Label lblURI;
        private System.Windows.Forms.TextBox txtUser;
        private System.Windows.Forms.Label lblUser;
        private System.Windows.Forms.TextBox txtOutput;
        private System.Windows.Forms.Button btnStart;
        private System.Windows.Forms.FolderBrowserDialog browser;
        private System.ComponentModel.BackgroundWorker pythonRun;
        private System.Windows.Forms.ProgressBar progress;
        private System.Windows.Forms.Button btnHe;
        private System.Windows.Forms.ComboBox txtHeadset;
        private System.Windows.Forms.Label lblHeadset;
    }
}

