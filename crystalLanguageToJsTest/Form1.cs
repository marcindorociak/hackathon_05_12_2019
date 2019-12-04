using System;
using System.Windows.Forms;
using CrystalLanguageToJsDll;


namespace CrystalLanguageToJs
{
    /// <summary>
    /// Project is based on ConvertDelphiToCSharp project due to
    /// Delphi language is similar to Crystal language used in Crystal Reports
    /// </summary>
    public class frmD2C : System.Windows.Forms.Form
	{
		private System.Windows.Forms.Button btnConvert;
		private System.Windows.Forms.RichTextBox tb1;
		private System.Windows.Forms.Label label1;
		private System.Windows.Forms.Label label2;
		private System.Windows.Forms.TextBox txtDelphiDotNetSourceFolder;
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

		public frmD2C()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//
			// TODO: Add any constructor code after InitializeComponent call
			//
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose( bool disposing )
		{
			if( disposing )
			{
				if (components != null) 
				{
					components.Dispose();
				}
			}
			base.Dispose( disposing );
		}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
            this.tb1 = new System.Windows.Forms.RichTextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.btnConvert = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.txtDelphiDotNetSourceFolder = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // tb1
            // 
            this.tb1.AutoSize = true;
            this.tb1.Dock = System.Windows.Forms.DockStyle.Bottom;
            this.tb1.Font = new System.Drawing.Font("Courier New", 8.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.tb1.Location = new System.Drawing.Point(0, 93);
            this.tb1.Name = "tb1";
            this.tb1.Size = new System.Drawing.Size(904, 536);
            this.tb1.TabIndex = 2;
            this.tb1.Text = "";
            this.tb1.WordWrap = false;
            // 
            // label1
            // 
            this.label1.Location = new System.Drawing.Point(8, 48);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(56, 32);
            this.label1.TabIndex = 3;
            this.label1.Text = "label1";
            // 
            // btnConvert
            // 
            this.btnConvert.Location = new System.Drawing.Point(608, 8);
            this.btnConvert.Name = "btnConvert";
            this.btnConvert.Size = new System.Drawing.Size(104, 32);
            this.btnConvert.TabIndex = 1;
            this.btnConvert.Text = "Convert";
            this.btnConvert.Click += new System.EventHandler(this.btnConvert_Click);
            // 
            // label2
            // 
            this.label2.Location = new System.Drawing.Point(80, 49);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(760, 24);
            this.label2.TabIndex = 5;
            this.label2.Text = "label2";
            // 
            // txtDelphiDotNetSourceFolder
            // 
            this.txtDelphiDotNetSourceFolder.Location = new System.Drawing.Point(88, 16);
            this.txtDelphiDotNetSourceFolder.Name = "txtDelphiDotNetSourceFolder";
            this.txtDelphiDotNetSourceFolder.Size = new System.Drawing.Size(456, 20);
            this.txtDelphiDotNetSourceFolder.TabIndex = 6;
            // 
            // frmD2C
            // 
            this.AutoScaleBaseSize = new System.Drawing.Size(5, 13);
            this.ClientSize = new System.Drawing.Size(904, 629);
            this.Controls.Add(this.txtDelphiDotNetSourceFolder);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.tb1);
            this.Controls.Add(this.btnConvert);
            this.Name = "frmD2C";
            this.Text = "Convert Crystal to JS";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

		}
		#endregion

		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		[STAThread]
		static void Main() 
		{
			Application.Run(new frmD2C());
		}

        private void btnConvert_Click(object sender, System.EventArgs e)
        {
            CrystalLanguageToJsDll.CrystalLanguageToJsDll convertClass = new CrystalLanguageToJsDll.CrystalLanguageToJsDll();
            tb1.Text = convertClass.ConvertCodeMain(tb1.Text);
        }

		private void Form1_Load(object sender, System.EventArgs e)
		{
			label1.Text = "";
			label2.Text = "Cut and paste Delphi unit into the text box, then Convert.";
		}
		
/*???*/

		
		
	}
}
