package cmd

import "testing"

func FuzzParse(f *testing.F) {
	f.Add("1+1")
	f.Add("")
	f.Fuzz(func(t *testing.T, input string) {
		Parse(input)
	})
}
