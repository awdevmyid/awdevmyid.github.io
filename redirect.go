func redirectToFreshman(w http.ResponseWriter, r *http.Request) {

	http.Redirect(w, r, "https://www.awdev.my.id", http.StatusSeeOther)

}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/", redirectToFreshman)

	http.ListenAndServe(":6000", mux)
}
