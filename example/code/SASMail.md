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


