# SASMail

## Macros(s):
### _SplitEmailParams
*No doc string*

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- | --- |
| In | Optional | None | Input macro var |
| Out | Optional | None | Output macro var |
| Bracket | Optional | YES | No docstring provided for argument |


### _SplitAttachments
*No doc string*

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- | --- |
| In | Optional | None | Macro var containing attachment locations |
| Out | Optional | None | Output macro var |


### SASMail
*<< strip the spaces
			*

#### Argument(s):

| Name | Type | Default Value | About |
| --- | --- | --- | --- | --- |
| To | Optional | None | Recipient(s), separated by spaces if mulitple |
| Subject | Optional | None | Subject of the email |
| From | Optional | NONE  | Defaults to your user@hefce account, this is also where replys will go if no Reply= is specified |
| Reply | Optional | NONE  | Where replies will go, default is the From= address |
| CC | Optional | None | Recipient(s), separated by spaces if mulitple |
| BCC | Optional | NONE | Recipient(s), separated by spaces if mulitple. The from account will always be BCC |
| Attach | Optional | NONE  | Attachments, separated by PIPE "|" if multiple |
| BodyFile | Optional | NONE  | Specifies a .txt file containing the body of the message, must be specified if Send = Y |
| Send | Optional | Y  | Whether to let the macro send the message for you, if N is specified then you must use a Datastep with "File SASMail" |
| ReadRcpt | Optional | N  | Specify Y to receive a read reciept, defaults to no |
| Importance | Optional | NORMAL  | Specify importance, defaults to normal |
| ContentType | Optional | text | No docstring provided for argument |


## Full code:
~~~~
*Macro to split space separated parameters and return a global
variable of them in quotes, all incased by brackets;
%Macro _SplitEmailParams(In=/*Input macro var*/, Out=/*Output macro var*/,Bracket=YES);
%local i;
	%if &Bracket=YES %then %Let Str =( ;
  %else %let Str = %str();
	%Do i = 1 %to %sysFunc(CountW(&In., |, s)); * |, s << used to cope with new lines in variables and make sure dots in addresses dont get  counted;
		%Let AddStr = %Scan(&In., &i., |, s);
		%Let Str = &Str."&AddStr.";
	%End;
	%if &Bracket=YES %then %Let Str = &Str);

	%Global &Out.;
	%Let &Out.=&Str.;
%MEnd _SplitEmailParams;

%Macro _SplitAttachments(In=/*Macro var containing attachment locations*/, Out=/*Output macro var*/);
	%local i;

	%Let Str =;
	%Do i = 1 %to %sysFunc(CountW(&In., |));
		%Let AddStr = %Scan(&In., &i., |);
		%Let Str = &Str. "&AddStr." ct='application/octet-stream' ;
	%End;


	%Global &Out.;
	%Let &Out.=&Str.;
%MEnd _SplitAttachments;



*Macro to set FileName Email settings and possibly send message;
*Comparisons of email addresses wrapped in quotes to mask hyphens and apostrophes;


%Macro SASMail(To=/*Recipient(s), separated by spaces if mulitple*/,
				Subject =/*Subject of the email*/,
				From=NONE /*Defaults to your user@hefce account, this is also where replys will go if no Reply= is specified*/,
				Reply=NONE /*Where replies will go, default is the From= address*/,
				CC=/*Recipient(s), separated by spaces if mulitple*/,
				BCC=NONE/*Recipient(s), separated by spaces if mulitple. The from account will always be BCC*/,
				Attach=NONE /*Attachments, separated by PIPE "|" if multiple*/,
				BodyFile=NONE /*Specifies a .txt file containing the body of the message, must be specified if Send = Y*/,
				Send=Y /*Whether to let the macro send the message for you, if N is specified then you must use a Datastep with "File SASMail"*/,
				ReadRcpt=N /*Specify Y to receive a read reciept, defaults to no*/,
				Importance=NORMAL /*Specify importance, defaults to normal*/,
				ContentType=text/plain
				);

	*Email system settings;
	Options EmailSys = SMTP EmailHost = "" EmailAuthProtocol = None;

	*Set some utility vars;
	%Let Colon=:;
	%Let Err = ERROR&Colon.;
	%Let Warn = WARNING&Colon.;

	*Try to determine the users email address;
	%Let UserEmail = NONE;
data _FmtOut;
set library._FmtOut (where=(FmtName in ("FNAME" "LNAME")) encoding="ASCII");
run;
	Proc SQL NoPrint;
		Create Table _UserEmail as
		Select a.Start as UserName, a.Label as FName, b.Label as LName,
			substr(a.Label, 1, 1) || "." || strip(b.Label) || "@officeforstudents.org.uk" as EmailAddress,
			Count(substr(a.Label, 1, 1) || "." || strip(b.Label) || "@officeforstudents.org.uk") as AddressCount
		From (Select Start, Label from _FmtOut where FMTName = "FNAME") as a
		Left Join (Select Start, Label from _FmtOut where FMTName = "LNAME") as b
		On a.Start = b.Start
		Where upcase(UserName) = upcase("&SysUserID.")
		Group by substr(a.Label, 1, 1) || "." || strip(b.Label) || "@officeforstudents.org.uk";
		
		Select Count(*)
		Into :_NumAddressFound
		From _UserEmail where FName ne "" 
							and LName ne ""
							and AddressCount = 1;
		
		%If %eval(&_NumAddressFound = 1) %then %do;
			Select EmailAddress
			Into :UserEmail separated by "" /*<< strip the spaces*/
			From _UserEmail where FName ne "" 
								and LName ne ""
								and AddressCount = 1;
		%End;
	Quit;

	Proc Datasets Lib=Work Nolist;
		Delete _FmtOut;
	Quit;

	*If email address couldnt be worked out (maybe multiples or no last name) and from=NONE
	then end the program;
	%If "&UserEmail." = "NONE" and "&From." = "NONE" %then %do;
		%Put &Err. Your @hefce email address could not be resolved from your username;
		%Put &Err. Check Work._UserEmail;
		%Put &Err. Please specify a "from" address using From=;
		%Abort Cancel;
	%End;

	*Delete _UserEmail if we get to this point;
	Proc Datasets Lib=Work Nolist;
		Delete _UserEmail;
	Quit;

	*Check BodyFile is provided if send = Y;
	%If %upcase(&Send.) = Y and %upcase("&BodyFile.") = "NONE" %then %do;
		%Put &Err You must specify a value for BodyFile if Send = Y;
		%Abort Cancel;
	%End;

	*Check values for importance are valid;
	%If %upcase(&Importance.) ne LOW and
		%upcase(&Importance.) ne NORMAL and
		%upcase(&Importance.) ne HIGH %then %do;
			%Put &Err. You must choose either Low, Normal or High for Importance=;
			%Abort Cancel;
	%End;
	
	*Split and prepare space seperated parameters;
	%_SplitEmailParams(In = &To., Out = _To);
	%_SplitEmailParams(In = &CC., Out = _CC);
	%If "&From." = "NONE" and "&BCC." = "NONE" %then %do;
		%_SplitEmailParams(In = &UserEmail., Out = _From); *From is not space separated (you cant have more than one), but the macro does prepare it properly;
		%_SplitEmailParams(In = &UserEmail., Out = _BCC);
	%End;
	%Else %if "&From." ne "NONE" and "&BCC." ne "NONE" %then %do;
		%_SplitEmailParams(In = &From., Out = _From);
		%_SplitEmailParams(In = &From. &BCC., Out = _BCC);
	%End;
	%Else %if "&From." ne "NONE" and "&BCC." = "NONE" %then %do;
		%_SplitEmailParams(In = &From., Out = _From);
		%_SplitEmailParams(In = &From., Out = _BCC);
	%End;
	%Else %if "&From." = "NONE" and "&BCC." ne "NONE" %then %do;
		%_SplitEmailParams(In = &UserEmail., Out = _From);
		%_SplitEmailParams(In = &UserEmail. &BCC., Out = _BCC);
	%End;

	
	*The _Attach var should include the "Attach=" option statement if attachments
	are being sent, otherwise set it to blank. SAS errors if Attach= is specified
	on the filename but no file is offered (unlike blank CC, To, etc);
	%If %upcase("&Attach.") ne "NONE" %then %do;
		%_SplitAttachments(In = &Attach., Out = _Attach);
		%Let _Attach = Attach = (&_Attach);
	%End;
	%Else %let _Attach=;
	
	*Set blank for read receipt variable if no, if yes set it to option value;
	%If %upcase(&ReadRcpt.) = N %then %Let _ReadRcpt =;
	%Else %if %upcase(&ReadRcpt.) = Y %then %let _ReadRcpt= ReadReceipt;
	%Else %do;
		%Put &Err ReadRcpt= must be either Y or N;
		%Abort Cancel;
	%End;

	*Set ("") for _Reply if Reply=NONE;
	%If %upcase(&Reply.) = NONE %then %let _Reply=("");
	%Else %let _Reply = "&Reply.";

	*Put quotes around other vars, just so its tidy in the filename statement!;
	%Let _Subject = "&Subject.";
	%Let _Importance = "&Importance";

	*Create the FileName statement;
	*Sender added to create consistent From: message in email. Masks username@hefce-sasX.ac.uk. A. Olsen - 03.04.2018;
	FileName SASMail Email To=&_To. Subject=&_Subject. From=&_From. Sender=&_From. Replyto=&_Reply.
							CC=&_CC. BCC=&_BCC.
							Importance=&_Importance.
							Content_type="&ContentType"
							&_ReadRcpt. &_Attach.;

	%Put FileName SASMail Email To=&_To. Subject=&_Subject. From=&_From. Sender=&_From. Replyto=&_Reply.
							CC=&_CC. BCC=&_BCC.
							Importance=&_Importance.
							Content_type="&ContentType"
							&_ReadRcpt. &_Attach.;

	*If Send=Y, send the email;
	%If %upcase(&Send.) = Y %then %do;
		Data _NULL_;
			File SASMail;
			InFile "&BodyFile." missover dlm='09'x;
			Format Line $4096.;
			Input Line;
			Put Line;
		Run;

		%Put NOTE&Colon. Email sent with From=&_From.;
	%End;
	
	*Delete the global vars made by _SplitEmailParams;
	%SymDel _To _CC _BCC;
	%If %upcase("&Attach.") ne "NONE" %then %symDel _Attach;
%MEnd SASMail;
~~~~