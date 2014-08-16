/*	Put in ISC license text here in a commit soon to signify that it's
	licensed under the aforementioned license.
*/

package main


import (
	"fmt"
	"strings"
	"time"
	"github.com/thoj/go-ircevent"
	"github.com/ndyakov/go-lastfm"
)
var (
	server			string	= "irc.iotek.org:6667"
        admins				= []string { "dami", "jmbi"}
	auth_users			= []string {}
	channel			string	= "#test"
	nickname		string	= "fapo"
	username		string	= "fapo"
	nickserv_pass		string	= ""
	cmdPrefix		string	= "."
	s_nick			string  = ""
	s_cmd			string  = ""
	nickmap				= make(map[string]string)
	lfm				= lastfm.New("", "")
)


//	check nickserv auth
func checkIdent (nick string, ircobj *irc.Connection) {
	ircobj.Privmsgf("nickserv", "STATUS %s", nick)
	return
}

//	bot functions selected here
func handleCmd (s_nick string, s_cmd []string, ircobj *irc.Connection) {

//	fmt.Println(s_nick)
//	fmt.Println(s_cmd)

	cmd	:= strings.Replace(s_cmd[0], cmdPrefix, "", 1)
	cmdArgs	:= s_cmd[1:]
	var msg string = ""

	fmt.Println(cmd)
	fmt.Println(cmdArgs)
//	fmt.Println(len(cmd))
//	fmt.Println(len(cmdArgs))

//	if len(cmd) < 2 { return }
//	switch {
//	case cmd[:2] == "set":
//	}
//	if msg != "" { ircobj.Privmsg(channel, msg) }
}

//	here be dragons
func main () {
/*	assign ident and connect	*/
	ircobj := irc.IRC(nickname, username)
	ircobj.Connect(server)
	ircobj.VerboseCallbackHandler = false

	ircobj.AddCallback("001", func(e *irc.Event) {
		if (ircobj.GetNick() != nickname) {}
		if (nickserv_pass != "") {
			ircobj.Privmsgf("nickserv", "identify %s",
			nickserv_pass)
			ircobj.Privmsg("hostserv", "on")
			time.Sleep(750 * time.Millisecond)
		}
		ircobj.Join(channel)
	})
	ircobj.AddCallback("NOTICE",  func(e *irc.Event) {
		if (e.Nick == "NickServ" &&
		strings.Split(e.Message(), " ")[2] == "3" && s_cmd != "") {
			// true auth
			fmt.Println(string(s_nick) + " is authed")
			handleCmd(s_nick, strings.Split(s_cmd, " "), ircobj)
			s_nick = ""
			s_cmd = ""
		}
	})
	ircobj.AddCallback("PRIVMSG", func(e *irc.Event) {
	// insert handlers
		if (strings.HasPrefix(e.Message(), cmdPrefix)) {
			s_nick = e.Nick
			s_cmd = e.Message()
			checkIdent(s_nick, ircobj)
		}
	time.Sleep(350 * time.Millisecond)
	})

	ircobj.Loop()
}
