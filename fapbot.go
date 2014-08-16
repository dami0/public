/*	Put in ISC license text here in a commit soon to signify that it's
	licensed under the aforementioned license.
*/

package main


import (
	"fmt"
	"time"
	"math"
	"strings"
	"strconv"
	"github.com/thoj/go-ircevent"
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
	fappers				= make(map[string][]string)
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

//	fmt.Println(cmd)
//	fmt.Println(cmdArgs)
//	fmt.Println(len(cmd))
//	fmt.Println(len(cmdArgs))

	if len(cmdArgs) < 1 { return }
	switch {
	case cmd == "set":
		if len(cmdArgs) < 4 { return }
		fappers[cmdArgs[0]] = cmdArgs[1:4]
		fmt.Println(fappers)
	case cmd == "len":
		date := fappers[cmdArgs[0]]
		if date == nil { return }
		year, _ := strconv.ParseInt(date[2], 10, 16)
		temp, _ := strconv.ParseInt(date[1], 10, 8)
		month := time.Month(temp)
		day, _ := strconv.ParseInt(date[0], 10, 8)
		tStart := time.Date(int(year), month, int(day), 0, 0, 0, 0,
			time.UTC)
		dt := int64(math.Floor(time.Since(tStart).Hours()/24))
		msg = strconv.FormatInt(dt, 10)
	case cmd == "del":
		delete(fappers, cmdArgs[0])
	}
	if msg != "" { ircobj.Privmsg(channel, msg) }
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
