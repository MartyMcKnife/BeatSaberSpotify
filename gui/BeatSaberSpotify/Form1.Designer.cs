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
            this.SuspendLayout();
            // 
            // lblPath
            // 
            this.lblPath.AutoSize = true;
            this.lblPath.Location = new System.Drawing.Point(28, 29);
            this.lblPath.Name = "lblPath";
            this.lblPath.Size = new System.Drawing.Size(145, 20);
            this.lblPath.TabIndex = 0;
            this.lblPath.Text = "Path to Beat Saber";
            // 
            // txtPath
            // 
            this.txtPath.Location = new System.Drawing.Point(189, 26);
            this.txtPath.Name = "txtPath";
            this.txtPath.Size = new System.Drawing.Size(258, 26);
            this.txtPath.TabIndex = 1;
            // 
            // btnExplore
            // 
            this.btnExplore.Location = new System.Drawing.Point(453, 25);
            this.btnExplore.Name = "btnExplore";
            this.btnExplore.Size = new System.Drawing.Size(32, 29);
            this.btnExplore.TabIndex = 2;
            this.btnExplore.Text = "...";
            this.btnExplore.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            this.btnExplore.UseVisualStyleBackColor = true;
            this.btnExplore.Click += new System.EventHandler(this.BtnExplore_Click);
            // 
            // btnHelp
            // 
            this.btnHelp.Location = new System.Drawing.Point(453, 66);
            this.btnHelp.Name = "btnHelp";
            this.btnHelp.Size = new System.Drawing.Size(32, 29);
            this.btnHelp.TabIndex = 5;
            this.btnHelp.Text = "?";
            this.btnHelp.TextAlign = System.Drawing.ContentAlignment.TopCenter;
            this.btnHelp.UseVisualStyleBackColor = true;
            this.btnHelp.Click += new System.EventHandler(this.Button2_Click);
            // 
            // txtURI
            // 
            this.txtURI.Location = new System.Drawing.Point(189, 67);
            this.txtURI.Name = "txtURI";
            this.txtURI.Size = new System.Drawing.Size(258, 26);
            this.txtURI.TabIndex = 4;
            this.txtURI.TextChanged += new System.EventHandler(this.TextBox2_TextChanged);
            // 
            // lblURI
            // 
            this.lblURI.AutoSize = true;
            this.lblURI.Location = new System.Drawing.Point(28, 70);
            this.lblURI.Name = "lblURI";
            this.lblURI.Size = new System.Drawing.Size(91, 20);
            this.lblURI.TabIndex = 3;
            this.lblURI.Text = "Spotify URI";
            this.lblURI.Click += new System.EventHandler(this.Label1_Click);
            // 
            // txtUser
            // 
            this.txtUser.Location = new System.Drawing.Point(189, 110);
            this.txtUser.Name = "txtUser";
            this.txtUser.Size = new System.Drawing.Size(258, 26);
            this.txtUser.TabIndex = 7;
            // 
            // lblUser
            // 
            this.lblUser.AutoSize = true;
            this.lblUser.Location = new System.Drawing.Point(28, 113);
            this.lblUser.Name = "lblUser";
            this.lblUser.Size = new System.Drawing.Size(83, 20);
            this.lblUser.TabIndex = 6;
            this.lblUser.Text = "Username";
            // 
            // txtOutput
            // 
            this.txtOutput.Location = new System.Drawing.Point(189, 190);
            this.txtOutput.Multiline = true;
            this.txtOutput.Name = "txtOutput";
            this.txtOutput.ReadOnly = true;
            this.txtOutput.ScrollBars = System.Windows.Forms.ScrollBars.Vertical;
            this.txtOutput.Size = new System.Drawing.Size(296, 96);
            this.txtOutput.TabIndex = 8;
            this.txtOutput.TextChanged += new System.EventHandler(this.TxtOutput_TextChanged);
            // 
            // btnStart
            // 
            this.btnStart.Location = new System.Drawing.Point(32, 190);
            this.btnStart.Name = "btnStart";
            this.btnStart.Size = new System.Drawing.Size(126, 41);
            this.btnStart.TabIndex = 9;
            this.btnStart.Text = "Start";
            this.btnStart.UseVisualStyleBackColor = true;
            this.btnStart.Click += new System.EventHandler(this.BtnStart_Click);
            // 
            // pythonRun
            // 
            this.pythonRun.DoWork += new System.ComponentModel.DoWorkEventHandler(this.BackgroundWorker1_DoWork);
            // 
            // progress
            // 
            this.progress.Location = new System.Drawing.Point(32, 151);
            this.progress.Name = "progress";
            this.progress.Size = new System.Drawing.Size(453, 23);
            this.progress.TabIndex = 10;
            // 
            // btnHe
            // 
            this.btnHe.Location = new System.Drawing.Point(32, 237);
            this.btnHe.Name = "btnHe";
            this.btnHe.Size = new System.Drawing.Size(126, 40);
            this.btnHe.TabIndex = 11;
            this.btnHe.Text = "Help";
            this.btnHe.UseVisualStyleBackColor = true;
            this.btnHe.Click += new System.EventHandler(this.BtnHe_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(9F, 20F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(510, 315);
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
            this.Name = "Form1";
            this.Text = "Form1";
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
    }
}

